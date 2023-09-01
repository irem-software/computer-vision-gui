from PyQt5 import QtCore, QtGui, QtWidgets, Qt
from PyQt5.QtWidgets import QFileDialog
from PyQt5.QtGui import QImage
import imutils
import time
import cv2
from PyQt5.QtWidgets import QVBoxLayout
from PyQt5.QtCore import Qt, QPoint, QRect
from PyQt5.QtGui import QPixmap, QPainter


class MainProgram(QtWidgets.QMainWindow):
    def __init__(self):
        super().__init__()

        self.recorder = None
        self.image = None
        self.pushButton_3 = None
        self.setupUi(self)

        self.window_width, self.window_height = 1920, 1000
        self.setMinimumSize(self.window_width, self.window_height)

        layout = QVBoxLayout()
        self.setLayout(layout)

        self.pix = QPixmap(self.rect().size())
        self.pix.fill(Qt.transparent)
        self.label.setPixmap(self.pix)

        self.cropRect = None
        self.isCropClicked = False
        self.x, self.y, self.width, self.height = None, None, None, None
        self.begin, self.destination = QRect(), QRect()
        self.isgrayclicked = False
        self.isScaleClicked = False
        self.isRecordClicked = False

        # TODO:
        #  - call the main process method

    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(1000, 600)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.gridLayout_2 = QtWidgets.QGridLayout(self.centralwidget)
        self.gridLayout_2.setObjectName("gridLayout_2")
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.label = QtWidgets.QLabel(self.centralwidget)
        self.label.setText("")
        self.label.setPixmap(QtGui.QPixmap("images/H.png"))
        self.label.setObjectName("label")
        self.horizontalLayout.addWidget(self.label)

        self.scale_width_label = QtWidgets.QLabel(self.centralwidget)
        self.scale_width_lineedit = QtWidgets.QLineEdit(self.centralwidget)
        self.scale_height_label = QtWidgets.QLabel(self.centralwidget)
        self.scale_height_lineedit = QtWidgets.QLineEdit(self.centralwidget)

        self.lb_width = QtWidgets.QLabel(self.centralwidget)
        self.lb_height = QtWidgets.QLabel(self.centralwidget)
        self.le_width = QtWidgets.QLineEdit(self.centralwidget)
        self.le_height = QtWidgets.QLineEdit(self.centralwidget)
        self.x_x = QtWidgets.QLabel(self.centralwidget)
        self.xLineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.y_y = QtWidgets.QLabel(self.centralwidget)
        self.yLineEdit = QtWidgets.QLineEdit(self.centralwidget)

        self.lb_width.setText("Height :")
        self.lb_height.setText("Width :")
        self.x_x.setText("x: ")
        self.y_y.setText("y: ")
        self.scale_height_label.setText("Height: ")
        self.scale_width_label.setText("Width:")

        self.lb_width.setGeometry(1650, 50, 100, 15)  # label,x,y,en,boy
        self.lb_height.setGeometry(1650, 100, 80, 15)  # label

        self.le_width.setGeometry(1700, 50, 40, 15)  # line-edit
        self.le_height.setGeometry(1700, 100, 40, 15)  # line-edit

        self.xLineEdit.setGeometry(1700, 150, 40, 15)  # line edit
        self.yLineEdit.setGeometry(1700, 200, 40, 15)  # line edit

        self.x_x.setGeometry(1650, 150, 40, 15)  # label
        self.y_y.setGeometry(1650, 200, 40, 15)  # label

        self.scale_width_label.setGeometry(1650, 330, 40, 15)  # label
        self.scale_height_label.setGeometry(1650, 370, 40, 15)  # label

        self.scale_width_lineedit.setGeometry(1700, 330, 40, 15)
        self.scale_height_lineedit.setGeometry(1700, 370, 40, 15)

        self.gray_button = QtWidgets.QPushButton(self.centralwidget)
        self.gray_button.setObjectName("GRAY")
        self.gray_button.setGeometry(1600, 500, 150, 60)

        # H264
        self.recordButton = QtWidgets.QPushButton(self.centralwidget)
        self.recordButton.setObjectName("RECORD")
        self.recordButton.setGeometry(1600, 600, 150, 70)

        # pushbutton-crop tanımlanmış
        self.pushButton_crop = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_crop.setObjectName("pushButton_crop")
        self.pushButton_crop.setGeometry(1650, 250, 100, 30)

        self.pushButton_scale = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_scale.setObjectName("pushButton_scale")
        self.pushButton_scale.setGeometry(1650, 420, 40, 15)

        self.pushButton_scale.clicked.connect(self.scale)
        self.pushButton_crop.clicked.connect(self.crop)
        self.gray_button.clicked.connect(self.convertGrayscale)
        self.pushButton_scale.setFixedSize(100, 30)

        self.verticalLayout = QtWidgets.QVBoxLayout()
        self.horizontalLayout.addLayout(self.verticalLayout)

        self.gridLayout = QtWidgets.QGridLayout()
        self.gridLayout.setObjectName("gridLayout")
        self.verticalSlider = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider.setObjectName("verticalSlider")
        self.gridLayout.addWidget(self.verticalSlider, 0, 0, 1, 1)
        self.verticalSlider_2 = QtWidgets.QSlider(self.centralwidget)
        self.verticalSlider_2.setOrientation(QtCore.Qt.Vertical)
        self.verticalSlider_2.setObjectName("verticalSlider_2")
        self.gridLayout.addWidget(self.verticalSlider_2, 0, 1, 1, 1)
        self.label_2 = QtWidgets.QLabel(self.centralwidget)
        self.label_2.setAlignment(QtCore.Qt.AlignCenter)
        self.label_2.setObjectName("label_2")
        self.gridLayout.addWidget(self.label_2, 1, 0, 1, 1)
        self.label_3 = QtWidgets.QLabel(self.centralwidget)
        self.label_3.setAlignment(QtCore.Qt.AlignCenter)
        self.label_3.setObjectName("label_3")
        self.gridLayout.addWidget(self.label_3, 1, 1, 1, 1)
        self.horizontalLayout.addLayout(self.gridLayout)
        self.gridLayout_2.addLayout(self.horizontalLayout, 0, 0, 1, 2)
        self.horizontalLayout_2 = QtWidgets.QHBoxLayout()
        self.horizontalLayout_2.setObjectName("horizontalLayout_2")

        self.pushButton = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton.setObjectName("pushButton")
        self.horizontalLayout_2.addWidget(self.pushButton)

        self.pushButton_2 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_2.setObjectName("pushButton_2")
        self.horizontalLayout_2.addWidget(self.pushButton_2)

        self.pushButton_5 = QtWidgets.QPushButton(self.centralwidget)
        self.pushButton_5.setObjectName("pushButton_5")
        self.horizontalLayout_2.addWidget(self.pushButton_5)

        self.gridLayout_2.addLayout(self.horizontalLayout_2, 1, 0, 1, 1)
        spacerItem = QtWidgets.QSpacerItem(313, 20, QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Minimum)
        self.gridLayout_2.addItem(spacerItem, 1, 1, 1, 1)
        MainWindow.setCentralWidget(self.centralwidget)
        self.statusbar = QtWidgets.QStatusBar(MainWindow)
        self.statusbar.setObjectName("statusbar")
        MainWindow.setStatusBar(self.statusbar)
        self.retranslateUi(MainWindow)
        self.verticalSlider.valueChanged['int'].connect(self.brightness_value)
        self.verticalSlider_2.valueChanged['int'].connect(self.blur_value)

        self.recordButton.clicked.connect(self.Record)
        self.pushButton_2.clicked.connect(self.openCamera)
        self.pushButton.clicked.connect(self.savePhoto)
        self.pushButton_5.clicked.connect(self.openVideo)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

        # Added code here
        self.filename = 'Snapshot  ' + str \
            (time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        self.tmp = None
        self.brightness_value_now = 0
        self.blur_value_now = 0
        self.fps = 0
        self.started = False

    def openCamera(self):
        """
         This function will load the camera device, obtain the image
         and set it to label using the setPhoto function
        """
        if self.started:
            self.started = False
            self.pushButton_2.setText('Start')
        else:
            self.started = True
            self.pushButton_2.setText('Stop')

        self.videoCapture = cv2.VideoCapture(0)
        cnt = 0

        while self.videoCapture.isOpened():

            ret, self.image = self.videoCapture.read()

            # self.image = imutils.resize(self.image, height=1400)
            if not ret:
                print("Video bitti")
                self.videoCapture.release()
                break

            if self.isCropClicked:
                self.image = self.image[self.y: self.y + self.height, self.x:self.x + self.width]
                print("cropping")

            if self.isScaleClicked:
                self.image = cv2.resize(self.image, (self.scale_width, self.scale_height))
                print("resizing")

            if self.isgrayclicked:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            if self.isRecordClicked:
                self.recorder.write(self.image)
                print("yazdi")

            cnt += 1

            self.update()
            if cv2.waitKey(25) & 0xFF == ord('q'):
                cv2.destroyAllWindows()
                break
            if not self.started:
                print('Loop break')
                self.videoCapture.release()
                break

    def openVideo(self):
        self.video = True
        self.videoname, _ = QFileDialog.getOpenFileName(self, "QFileDialog.getOpenFileName()", "",
                                                        "Mp4 Files (*.mp4);;All Files (*)")
        if self.videoname:
            print(self.videoname)

        self.videoCapture = cv2.VideoCapture(self.videoname)

        cnt = 0
        frames_to_count = 20
        st = 0
        fps = 0

        while self.videoCapture.isOpened():
            QtWidgets.QApplication.processEvents()
            ret, self.image = self.videoCapture.read()

            if not ret:
                print("Video bitti")
                self.videoCapture.release()
                break

            if self.isCropClicked:
                self.image = self.image[self.y: self.y + self.height, self.x:self.x + self.width]

            if self.isScaleClicked:
                self.image = cv2.resize(self.image, (self.scale_width, self.scale_height))

            if self.isgrayclicked:
                self.image = cv2.cvtColor(self.image, cv2.COLOR_BGR2GRAY)

            if cnt == frames_to_count:
                try:
                    self.fps = round(frames_to_count / (time.time() - st))

                    st = time.time()
                    cnt = 0
                except:
                    pass

            cnt += 1

            self.update()
            key = cv2.waitKey(1) & 0xFF

    def Record(self):
        if self.isRecordClicked:
            self.isRecordClicked = False
            self.recordButton.setText("RECORD")
            self.recorder.release()
            print("stop basıldı")
        else:
            self.isRecordClicked = True
            self.recordButton.setText("STOP")

            fourcc = cv2.VideoWriter_fourcc(*'H264')
            kayit_dosyasi = 'kayit2.mp4'
            boyut = self.image.shape[:2]
            print(self.image.shape)
            self.recorder = cv2.VideoWriter(kayit_dosyasi, fourcc, 30.0, (640, 480))
            print("record basıldı")

    def setPhoto(self, image):
        """ This function will take image input and resize it
            only for display purpose and convert it to QImage
            to set at the label.
        """

        if self.isgrayclicked:

            self.image = QImage(self.image, self.image.shape[1], self.image.shape[0], self.image.strides[0],
                                QImage.Format_Grayscale8)
            self.label.setPixmap(QtGui.QPixmap.fromImage(self.image))
        else:
            self.tmp = image
            frame = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
            image = QImage(frame, frame.shape[1], frame.shape[0], frame.strides[0], QImage.Format_RGB888)
            self.label.setPixmap(QtGui.QPixmap.fromImage(image))

    def brightness_value(self, value):
        """ This function will take value from the slider
            for the brightness from 0 to 99
        """
        self.brightness_value_now = value
        print('Brightness: ', value)
        self.update()

    def blur_value(self, value):
        """ This function will take value from the slider
            for the blur from 0 to 99 """
        self.blur_value_now = value
        print('Blur: ', value)
        self.update()

    def changeBrightness(self, img, value):
        """ This function will take an image (img) and the brightness
            value. It will perform the brightness change using OpenCv
            and after split, will merge the img and return it.
        """
        hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
        h, s, v = cv2.split(hsv)
        lim = 255 - value
        v[v > lim] = 255
        v[v <= lim] += value
        final_hsv = cv2.merge((h, s, v))
        img = cv2.cvtColor(final_hsv, cv2.COLOR_HSV2BGR)
        return img

    def changeBlur(self, img, value):
        """ This function will take the img image and blur values as inputs.
            After perform blur operation using opencv function, it returns
            the image img.
        """
        kernel_size = (value + 1, value + 1)  # +1 is to avoid 0
        img = cv2.blur(img, kernel_size)
        return img

    def update(self):
        """ This function will update the photo according to the
            current values of blur and brightness and set it to photo label.
        """
        if not self.isgrayclicked:
            self.image = self.changeBrightness(self.image, self.brightness_value_now)
            self.image = self.changeBlur(self.image, self.blur_value_now)
        self.setPhoto(self.image)

    def scale(self):
        self.isScaleClicked = True
        self.scale_width = int(self.scale_width_lineedit.text())
        self.scale_height = int(self.scale_height_lineedit.text())

        print("Scale info read")

    def convertGrayscale(self):
        if self.isgrayclicked:
            self.isgrayclicked = False
            self.gray_button.setText("GRAY")
            self.verticalSlider_2.setEnabled(True)
            self.verticalSlider.setEnabled(True)
        else:
            self.isgrayclicked = True
            self.gray_button.setText("BACK TO ORIGINAL")
            self.verticalSlider_2.setEnabled(False)
            self.verticalSlider.setEnabled(False)

    def crop(self):
        self.width = int(self.le_width.text())
        self.height = int(self.le_height.text())
        self.x = int(self.xLineEdit.text())
        self.y = int(self.yLineEdit.text())

        self.isCropClicked = True

    def savePhoto(self):
        """ This function will save the image"""
        self.filename = 'Snapshot ' + str(time.strftime("%Y-%b-%d at %H.%M.%S %p")) + '.png'
        cv2.imwrite(self.filename, self.tmp)
        print('Image saved as:', self.filename)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "iremin uygulaması"))
        self.label_2.setText(_translate("MainWindow", "Brightness"))
        self.label_3.setText(_translate("MainWindow", "Blur"))
        self.pushButton.setText(_translate("MainWindow", "Take picture"))
        self.pushButton_2.setText(_translate("MainWindow", "camera"))
        self.pushButton_5.setText(_translate("MainWindow", "video"))
        self.pushButton_crop.setText(_translate("MainWindow", "crop"))
        self.pushButton_scale.setText(_translate("MainWindow", "Scale"))
        self.gray_button.setText(_translate("MainWindow", "GRAY "))
        self.recordButton.setText(_translate("MainWindow", "RECORD"))


if __name__ == "__main__":
    import sys

    app = QtWidgets.QApplication(sys.argv)
    MainWindow = MainProgram()
    MainWindow.show()
    sys.exit(app.exec_())
