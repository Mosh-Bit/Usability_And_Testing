import sys
# import blink_detector_face_orientation
from PyQt5.QtWidgets import QApplication, QWidget, QVBoxLayout, QPushButton, QLabel, QRadioButton, QButtonGroup, QMessageBox, QHBoxLayout, QSlider, QStyle, QFileDialog, QSizePolicy, QMainWindow, QSizePolicy, QAction, qApp
from PyQt5.QtMultimedia import QMediaPlayer, QMediaContent
from PyQt5.QtMultimediaWidgets import QVideoWidget
from PyQt5.QtCore import Qt, QUrl

""" Sources
 https://www.codecguide.com/download_k-lite_codec_pack_basic.htm for Video encodings
 https://wiki.qt.io/How_to_Use_QPushButton
 https://doc.qt.io/qt-5/qvideowidget.html
"""

class VideoPlayer(QWidget):
    def __init__(self):
        super().__init__()

        self.setWindowTitle("Usability & Testing - Video Player")
        self.setGeometry(100, 100, 800, 600)

        self.mediaPlayer = QMediaPlayer(None, QMediaPlayer.VideoSurface)

        self.videoWidget = QVideoWidget()

        self.playButton = QPushButton("Play")
        self.playButton.setEnabled(False)
        self.playButton.clicked.connect(self.playVideo)

        self.pauseButton = QPushButton("Pause")
        self.pauseButton.setEnabled(False)
        self.pauseButton.clicked.connect(self.pauseVideo)

        self.nextButton = QPushButton("Next -> Questionaire")
        self.nextButton.setEnabled(False)
        self.nextButton.clicked.connect(self.showNextSlide)
        self.nextButton.clicked.connect(self.pauseVideo)

        self.layout = QVBoxLayout()
        self.layout.addWidget(self.videoWidget)

        buttonLayout = QHBoxLayout()
        buttonLayout.addWidget(self.playButton)
        buttonLayout.addWidget(self.pauseButton)
        buttonLayout.addWidget(self.nextButton)

        self.layout.addLayout(buttonLayout)

        self.setLayout(self.layout)

        self.mediaPlayer.setVideoOutput(self.videoWidget)
        self.mediaPlayer.stateChanged.connect(self.mediaStateChanged)
        self.mediaPlayer.positionChanged.connect(self.positionChanged)
        self.mediaPlayer.durationChanged.connect(self.durationChanged)

        self.nextSlide = None  # Initialize as None

    
    def openFile(self):
        file, _ = QFileDialog.getOpenFileName(self, "Open Video", "../Videos/")
        if file != '':
            self.mediaPlayer.setMedia(QMediaContent(QUrl.fromLocalFile(file)))
            self.playButton.setEnabled(True)
            self.pauseButton.setEnabled(True)
            self.nextButton.setEnabled(True)

    def playVideo(self):
        self.mediaPlayer.play()

    def pauseVideo(self):
        self.mediaPlayer.pause()

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
        self.setGeometry(100, 100, 400, 300)

        self.question1 = QLabel("Question 1: Did the ad appeal to you?")

        self.q1_answer1_radio = QRadioButton("Option 1")
        self.q1_answer2_radio = QRadioButton("Option 2")
        self.q1_answer3_radio = QRadioButton("Option 3")

        self.question2 = QLabel("Question 2: Sample Question?")

        self.q2_answer1_radio = QRadioButton("Option 1")
        self.q2_answer2_radio = QRadioButton("Option 2")
        self.q2_answer3_radio = QRadioButton("Option 3")

        self.question3 = QLabel("Question 3: Sample Question?")

        self.q3_answer1_radio = QRadioButton("Option 1")
        self.q3_answer2_radio = QRadioButton("Option 2")
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
        selected_button = self.buttonGroup.checkedButton()
        if selected_button:
            answer = selected_button.text()
            QMessageBox.information(self, "Submission", f"Selected Answer: {answer}")
        else:
            QMessageBox.warning(self, "Submission", "Please select an answer.")
       
if __name__ == '__main__':
    app = QApplication(sys.argv)
    videoPlayer = VideoPlayer()
    videoPlayer.openFile()
    videoPlayer.show()
    sys.exit(app.exec_())
