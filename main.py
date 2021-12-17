import tkinter as tk
from tkinter import filedialog
from PIL import ImageTk, Image
import cv2
import face_recognition
import dlib
from scipy.spatial.distance import pdist


def UploadAction(event=None):
    filePath = filedialog.askopenfilename(filetypes=[("JPEG image files", ".jpg")])
    return filePath
# button = tk.Button(root, text='Open', command=UploadAction)
# button.pack()


def OpenCvImageAndCount(image_path):
    face_cascade = cv2.CascadeClassifier('C:/PythonProjects/faceComparing/venv/Lib/site-packages/cv2/data/haarcascade_frontalface_alt2.xml')
    image = cv2.imread(image_path)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    faces = face_cascade.detectMultiScale(
        gray,
        scaleFactor=1.1,
        minNeighbors=5,
        minSize=(10, 10)
    )
    faces_detected = len(faces)
    # Рисуем квадраты вокруг лиц
    for (x, y, w, h) in faces:
        cv2.rectangle(image, (x, y), (x + w, y + h), (80, 160, 255), 2)
    return image, faces_detected


if __name__ == '__main__':
    vecLeft = []
    vecRight = []
    leftDownloaded = False
    rightDownloaded = False
    rate = 0.6

    def compare():
        if leftDownloaded and rightDownloaded:
            return pdist([vecLeft, vecRight], 'euclidean')
        return None


    detector = dlib.get_frontal_face_detector()

    window = tk.Tk()
    window.resizable(False, False)
    window.title("Сравнение лиц")

    # > header
    frameHeader = tk.Frame(master=window, width=1000, height=50, bg="#aa0000")
    frameHeader.pack_propagate(False)
    frameHeader.pack(fill=tk.BOTH, side=tk.TOP)

    # > > header text
    label = tk.Label(master=frameHeader, text="Выберите два изображения с лицом на каждом")
    label.pack(fill=tk.BOTH, side=tk.TOP, anchor=tk.CENTER, expand=True)

    # > body
    frameBody = tk.Frame(master=window, width=1000, height=450, bg="#aa3300")
    frameBody.pack_propagate(False)
    frameBody.pack(fill=tk.BOTH, side=tk.TOP)

    # > > left image frame
    frameLeft = tk.Frame(master=frameBody, width=500, height=350, bg="#44aa00")
    frameLeft.pack_propagate(False)
    frameLeft.pack(fill=tk.BOTH, side=tk.LEFT)

    # > > > left image
    frameLeftImage = tk.Label(master=frameLeft, width=500, height=300)
    def SetLeftImage(path, width, height):
        imageLeft = Image.open(path)
        imageLeft = imageLeft.resize((width, height))
        imageLeft = ImageTk.PhotoImage(imageLeft)
        frameLeftImage.configure(image=imageLeft)
        frameLeftImage.image = imageLeft
    def SetLeftImageFromOpencv(img, width, height):
        imageLeft = Image.fromarray(img)
        imageLeft = imageLeft.resize((width, height))
        imageLeft = ImageTk.PhotoImage(imageLeft)
        frameLeftImage.configure(image=imageLeft)
        frameLeftImage.image = imageLeft
    SetLeftImage('assets/empty.jpg', 500, 300)
    frameLeftImage.pack_propagate(False)
    frameLeftImage.pack(fill=tk.BOTH, side=tk.TOP)

    # > > > left button frame
    frameLeftButton = tk.Frame(master=frameLeft, width=500, height=75, bg="#aaaa00")
    frameLeftButton.pack_propagate(False)
    frameLeftButton.pack(fill=tk.BOTH, side=tk.TOP)

    # > > > > left button
    def LeftSetup():
        global vecLeft, leftDownloaded
        path = UploadAction()
        if not path.endswith('.jpg'):
            labelLeftText['text'] = 'Неверный тип файла'
            leftDownloaded = False
            footerText['text'] = f'Нет двух загруженных изображений'
            return
        img = cv2.imread(path)
        vector = face_recognition.face_encodings(img)
        face_rect = detector(img, 1)
        faces = len(vector)
        for face in face_rect:
            cv2.rectangle(img, (face.left(), face.top()), (face.right(), face.bottom()),
                          (0, 255, 0), 7)
        if faces != 1:
            leftDownloaded = False
            if faces > 1:
                labelLeftText['text'] = f'Лиц на изображении: {faces} \nВыберите изображение с одним лицом'
            if faces == 0:
                labelLeftText['text'] = f'На изображении не найдено лиц'
            SetLeftImageFromOpencv(img, 500, 300)
            footerText['text'] = f'Нет двух загруженных изображений'
            return

        leftDownloaded = True
        vecLeft = vector[0]
        if faces != len(face_rect):
            labelLeftText['text'] += '\nВнимание: на изображении лица помечены некорректно'
        result = compare()
        if not(result is None):
            res = result[0] < rate
            if res:
                footerText['text'] = f'На изображениях один человек\n({result[0]})'
            else:
                footerText['text'] = f'На изображениях разный человек\n({result[0]})'
        else:
            footerText['text'] = f'Нет двух загруженных изображений'
        labelLeftText['text'] = 'Изображение загружено успешно'
        SetLeftImageFromOpencv(img, 500, 300)
    buttonLeft = tk.Button(master=frameLeftButton, text="Загрузить изображение", width=500, height=75, command=LeftSetup)
    buttonLeft.pack(fill=tk.BOTH, side=tk.TOP)

    # > > > left text frame
    frameLeftText = tk.Frame(master=frameLeft, width=500, height=75, bg="#44aa00")
    frameLeftText.pack_propagate(False)
    frameLeftText.pack(fill=tk.BOTH, side=tk.TOP)

    # > > > > left text
    labelLeftText = tk.Label(master=frameLeftText, text="Изображение не загружено", width=500, height=75, borderwidth=2, relief="solid")
    labelLeftText.pack(fill=tk.BOTH, side=tk.LEFT, anchor=tk.CENTER, expand=True)

    # > > right image frame
    frameRight = tk.Frame(master=frameBody, width=500, height=350, bg="#00aa44")
    frameRight.pack_propagate(False)
    frameRight.pack(fill=tk.BOTH, side=tk.LEFT)

    # > > > right image
    frameRightImage = tk.Label(master=frameRight, width=500, height=300)
    def SetRightImage(path, width, height):
        imageRight = Image.open(path)
        imageRight = imageRight.resize((width, height))
        imageRight = ImageTk.PhotoImage(imageRight)
        frameRightImage.configure(image=imageRight)
        frameRightImage.image = imageRight
    def SetRightImageFromOpencv(img, width, height):
        imageRight = Image.fromarray(img)
        imageRight = imageRight.resize((width, height))
        imageRight = ImageTk.PhotoImage(imageRight)
        frameRightImage.configure(image=imageRight)
        frameRightImage.image = imageRight
    SetRightImage('assets/empty.jpg', 500, 300)
    frameRightImage.pack_propagate(False)
    frameRightImage.pack(fill=tk.BOTH, side=tk.TOP)

    # > > > right button frame
    frameRightButton = tk.Frame(master=frameRight, width=500, height=75, bg="#aaaa00")
    frameRightButton.pack_propagate(False)
    frameRightButton.pack(fill=tk.BOTH, side=tk.TOP)

    # > > > > right button
    def RightSetup():
        global vecRight, rightDownloaded
        path = UploadAction()
        if not path.endswith('.jpg'):
            labelRightText['text'] = 'Неверный тип файла'
            rightDownloaded = False
            footerText['text'] = f'Нет двух загруженных изображений'
            return
        img = cv2.imread(path)
        vector = face_recognition.face_encodings(img)
        face_rect = detector(img, 1)
        faces = len(vector)
        for face in face_rect:
            cv2.rectangle(img, (face.left(), face.top()), (face.right(), face.bottom()),
                          (0, 255, 0), 7)
        if faces != 1:
            if faces > 1:
                labelRightText['text'] = f'Лиц на изображении: {faces} \nВыберите изображение с одним лицом'
            if faces == 0:
                labelRightText['text'] = f'На изображении не найдено лиц'
            SetRightImageFromOpencv(img, 500, 300)
            rightDownloaded = False
            footerText['text'] = f'Нет двух загруженных изображений'
            return
        rightDownloaded = True
        vecRight = vector[0]
        if faces != len(face_rect):
            labelRightText['text'] += '\nВнимание: на изображении лица помечены некорректно'
        result = compare()
        if not(result is None):
            res = result[0] < rate
            if res:
                footerText['text'] = f'На изображениях один человек\n({result[0]})'
            else:
                footerText['text'] = f'На изображениях разный человек\n({result[0]})'
        else:
            footerText['text'] = f'Нет двух загруженных изображений'
        labelRightText['text'] = 'Изображение загружено успешно'
        SetRightImageFromOpencv(img, 500, 300)
    buttonRight = tk.Button(master=frameRightButton, text="Загрузить изображение", width=500, height=75, command=RightSetup)
    buttonRight.pack(fill=tk.BOTH, side=tk.TOP)

    # > > > right text frame
    frameRightText = tk.Frame(master=frameRight, width=500, height=75, bg="#44aa00")
    frameRightText.pack_propagate(False)
    frameRightText.pack(fill=tk.BOTH, side=tk.TOP)

    # > > > > right text
    labelRightText = tk.Label(master=frameRightText, text="Изображение не загружено", width=500, height=75, borderwidth=2, relief="solid")
    labelRightText.pack(fill=tk.BOTH, side=tk.LEFT, anchor=tk.CENTER, expand=True)

    # > footer
    frameFooter = tk.Frame(master=window, width=1000, height=70, bg="#aa0033")
    frameFooter.pack_propagate(False)
    frameFooter.pack(fill=tk.BOTH, side=tk.TOP)

    # > > footer text
    footerText = tk.Label(master=frameFooter, text=f'Нет двух загруженных изображений', width=500, height=75, borderwidth=2, relief="solid")
    footerText.pack(fill=tk.BOTH, side=tk.LEFT, anchor=tk.CENTER, expand=True)

    window.mainloop()

