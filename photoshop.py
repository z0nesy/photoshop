import os
from PyQt5.QtWidgets import (
    QApplication, QWidget, QFileDialog,
    QLabel, QPushButton, QListWidget,
    QHBoxLayout, QVBoxLayout
)

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QPixmap
from PIL import Image
from PIL import ImageFilter

app = QApplication([])
win = QWidget()
win.resize (700,500)
win.setWindowTitle("easy editor")
lb_image = QLabel("картинка")
btn_dir = QPushButton ("папка")
lw_files = QListWidget()

btn_left = QPushButton("Ліво")
btn_right = QPushButton("Право")
btn_flip = QPushButton("Дзеркало")
btn_sharp = QPushButton("Різкість")
btn_bw = QPushButton("Ч/Б")

row = QHBoxLayout()
col1 = QVBoxLayout()
col2 = QVBoxLayout()
col1.addWidget(btn_dir)
col1.addWidget(lw_files)
col2.addWidget(lb_image, 95)

row_tool = QHBoxLayout()
row_tool.addWidget(btn_left)
row_tool.addWidget(btn_right)
row_tool.addWidget(btn_flip)
row_tool.addWidget(btn_sharp)
row_tool.addWidget(btn_bw)
col2.addLayout(row_tool)

row.addLayout(col1, 20) #25
row.addLayout(col2, 80) #75
win.setLayout(row)

workdir = ''

def filter_f(files, extensions):
    result = list()
    for filename in files:
        for ext in extensions:
            if filename.endswith(ext):
                result.append(filename)
    return result


def choose_work_dir():
    global workdir
    workdir = QFileDialog.getExistingDirectory()


def show_file_nemes_list():
    extensions = [".jpg", ".jpeg", ".png", "raw", ".gif", ".bmp"]
    choose_work_dir()
    filenames = filter_f(os.listdir(workdir), extensions)
    lw_files.clear()
    for filename in filenames:
        lw_files.addItem(filename)



btn_dir.clicked.connect(show_file_nemes_list)


class ImageProcessor():
    def __init__(self):
        self.Image = None
        self.dir = None
        self.filename = None
        self.save_dir = "Modified/"

    def LoadImage(self, dir, filename):
        self.dir = dir
        self.filename = filename
        image_path = os.path.join(dir, filename)
        self.image = Image.open(image_path)

    def showImage(self, path):
        lb_image.hide()
        pixmapimage = QPixmap(path)
        w, h = lb_image.width(), lb_image.height()
        pixmapimage = pixmapimage.scaled(w, h, Qt.KeepAspectRatio)
        lb_image.setPixmap(pixmapimage)
        lb_image.show()


    def saveImage(self):
        '''зберігає копію в підпабці'''
        path = os.path.join(workdir, self.save_dir)
        if not (os.path.exists(path) or os.path.isdir(path)):
            os.mkdir(path)
        image_path = os.path.join(path, self.filename)
        self.image.save(image_path)

    def do_bw(self):
        self.image = self.image.convert("L")
        self.saveImage()
        image_path = os.path.join(workdir, self.save_dir, self.filename)
        self.showImage(image_path)

    def do_right(self):
        self.image = self.image.transpose(Image.ROTATE_270)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)
    
    def do_left(self):
        self.image = self.image.transpose(Image.ROTATE_90)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)

    def do_sharp(self):
        self.image = self.image.filter(ImageFilter.BLUR)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)


    def do_flip(self):
        self.image = self.image.transpose(Image.FLIP_LEFT_RIGHT)
        self.saveImage()
        image_path = os.path.join(
            workdir, self.save_dir, self.filename
        )
        self.showImage(image_path)



work_image = ImageProcessor()


def showChousenImage():
    if lw_files.currentRow() >= 0:
        filename = lw_files.currentItem().text()
        work_image.LoadImage(workdir, filename)
        image_path = os.path.join(work_image.dir, work_image.filename)
        work_image.showImage(image_path)

lw_files.currentRowChanged.connect(showChousenImage)
btn_bw.clicked.connect(work_image.do_bw)
btn_right.clicked.connect(work_image.do_right)
btn_flip.clicked.connect(work_image.do_flip)
btn_left.clicked.connect(work_image.do_left)
btn_sharp.clicked.connect(work_image.do_sharp)
win.show()
app.exec_()