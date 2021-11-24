import sys
import os
from PIL import Image
import cv2
#from PIL.ImageQt import ImageQt
import numpy as np
from PySide6.QtWidgets import QApplication, QMainWindow, QSlider, QLabel
from PySide6.QtGui import QPixmap, QImage
from opacity_ui import Ui_MainWindow


class OpacityWindow(QMainWindow):
    def __init__(self):
        super(OpacityWindow, self).__init__()
        self.ui = Ui_MainWindow()
        self.ui.setupUi(self)

        # slider
        self.ui.verticalSlider.setMinimum(0)
        self.ui.verticalSlider.setMaximum(1000)
        self.ui.verticalSlider.setTickInterval(100)
        self.ui.verticalSlider.setTickPosition(QSlider.TicksLeft)

        # whenever the slider changes, execute the opacity change
        self.ui.verticalSlider.valueChanged.connect(self.opacity_change)

        # load image
        self.image_folder = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'images'))

        # convert image to numpy array
        self.image_array = Image.open(os.path.join(self.image_folder, "black_square.png")).convert('L')
        # self.image_array = np.uint8(np.asarray(self.image_array))
        self.image_array = np.asarray(self.image_array)

        pixmap = self.convert_np_to_pixmap(self.image_array)

        self.ui.label.setPixmap(pixmap)

    def convert_np_to_pixmap(self, numpy_array):
        # convert to cv2
        frame = cv2.cvtColor(numpy_array, cv2.COLOR_GRAY2RGB)

        # convert to qimage
        h, w = numpy_array.shape[:2]
        bytes_per_line = 3 * w
        qimage = QImage(frame.data, w, h, bytes_per_line, QImage.Format.Format_RGB888)

        # convert to pixmap
        pixmap = QPixmap.fromImage(qimage)

        return pixmap

    def opacity_change(self):
        x = self.ui.verticalSlider.value()
        print("{}^2 = {}".format(x, x**2))


if __name__ == "__main__":
    app = QApplication([])

    window = OpacityWindow()
    window.show()

    sys.exit(app.exec())
