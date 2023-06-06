import sys
import csv
# import blink_detector_face_orientation
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QRadioButton, QButtonGroup, QMessageBox, QHBoxLayout, QSlider, QStyle, QFileDialog, QSizePolicy, QMainWindow, QSizePolicy, QAction, qApp
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl
from PyQt5.QtGui import QKeySequence
from PyQt5.QtWidgets import QShortcut

""" 
Sources:
    for Video & Audio encodings:
    https://www.codecguide.com/download_k-lite_codec_pack_basic.htm
    Qt5 Tutorials:
    https://wiki.qt.io/How_to_Use_QPushButton
    https://doc.qt.io/qt-5/qvideowidget.html
"""

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Usability & Testing - Video Player")
        # self.setGeometry(100, 100, 800, 600)
        self.showFullScreen()

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

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
        self.nextButton.setEnabled(False)
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

        self.nextSlide = None  # Initialize as None

    
    def openFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Video", "Videos/")
        if file != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.playButton.setEnabled(True)
            # self.pauseButton.setEnabled(True)
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

    def showNextSlide(self):
        self.close()
        self.nextSlide = SlideWidget()
        self.nextSlide.show()

class SlideWidget(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Slide")
        # self.setGeometry(100, 100, 400, 300)
        self.showFullScreen

        self.question1 = QLabel("Question 1: General interest in the product category")

        self.q1_answer1_radio = QRadioButton("Agree")
        self.q1_answer2_radio = QRadioButton("Don't Agree")
        self.q1_answer3_radio = QRadioButton("Neutral")
        # think about slider

        self.question2 = QLabel("Question 2: Was it interesting to watch?")

        self.q2_answer1_radio = QRadioButton("Yes")
        self.q2_answer2_radio = QRadioButton("No")
        self.q2_answer3_radio = QRadioButton("Neutral")
        # remove neutral

        self.question3 = QLabel("Question 3: Positive or Negative Emotion?")

        self.q3_answer1_radio = QRadioButton("Positive")
        self.q3_answer2_radio = QRadioButton("Negative")
        self.q3_answer3_radio = QRadioButton("Option 3")

        self.q1_buttonGroup = QButtonGroup()
        self.q2_buttonGroup = QButtonGroup()
        self.q3_buttonGroup = QButtonGroup()

        self.q1_buttonGroup.addButton(self.q1_answer1_radio)
        self.q1_buttonGroup.addButton(self.q1_answer2_radio)
        self.q1_buttonGroup.addButton(self.q1_answer3_radio)
        self.q2_buttonGroup.addButton(self.q2_answer1_radio)
        self.q2_buttonGroup.addButton(self.q2_answer2_radio)
        self.q2_buttonGroup.addButton(self.q2_answer3_radio)
        self.q3_buttonGroup.addButton(self.q3_answer1_radio)
        self.q3_buttonGroup.addButton(self.q3_answer2_radio)
        self.q3_buttonGroup.addButton(self.q3_answer3_radio)

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

        layout = QVBoxLayout()
        layout.addWidget(self.question1)
        layout.addWidget(self.q1_answer1_radio)
        layout.addWidget(self.q1_answer2_radio)
        layout.addWidget(self.q1_answer3_radio)
        layout.addWidget(self.question2)
        layout.addWidget(self.q2_answer1_radio)
        layout.addWidget(self.q2_answer2_radio)
        layout.addWidget(self.q2_answer3_radio)
        layout.addWidget(self.question3)
        layout.addWidget(self.q3_answer1_radio)
        layout.addWidget(self.q3_answer2_radio)
        layout.addWidget(self.q3_answer3_radio)
        layout.addWidget(self.submitButton)

        self.setLayout(layout)

    def submitAnswers(self):
        selected_button_1 = self.q1_buttonGroup.checkedButton()
        selected_button_2 = self.q2_buttonGroup.checkedButton()
        selected_button_3 = self.q3_buttonGroup.checkedButton()
        if (selected_button_1):
            if(selected_button_2):
                if(selected_button_3):
                        answer_1 = selected_button_1.text()
                        answer_2 = selected_button_2.text()
                        answer_3 = selected_button_3.text()
                else:
                    QMessageBox.warning(self, "Submission", "Please select an answer in block 3.")
            else:
                QMessageBox.warning(self, "Submission", "Please select an answer in block 2")
        

            data = [
            ["Answer 1: ", answer_1],
            ["Answer 2: ", answer_2],
            ["Answer 3: ", answer_3]
            ]
            self.openCSV(data)
            message_box = QMessageBox(QMessageBox.Information, "Submission", f"Selected Answers: {answer_1, answer_2, answer_3}", QMessageBox.Close)
            message_box.exec_()
            self.close()
        else:
            QMessageBox.warning(self, "Submission", "Please select an answer in block 1.")

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

if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoPlayer = VideoPlayer()
    videoPlayer.openFile()
    videoPlayer.show()
    sys.exit(app.exec_())