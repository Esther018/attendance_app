import tkinter as tk
from tkinter import *
import cv2
import csv
import numpy as np
import os
from PIL import Image, ImageTk
import time
from tkinter import messagebox as mess
from tkinter import ttk
import pandas as pd
import datetime
from tkinter import filedialog

def is_number(s):
    try:
        float(s)
        return True
    except ValueError:
        pass

    try:
        import unicodedata
        unicodedata.numeric(s)
        return True
    except (TypeError, ValueError):
        pass

    return False

def assure_path_exists(path):
    dir = os.path.dirname(path)
    if not os.path.exists(dir):
        os.makedirs(dir)

#check for haarcascade file
def check_haarcascadefile():
    exists = os.path.isfile("haarcascade_frontalface_default.xml")
    if exists:
        pass
    else:
        mess._show(title='Cascade file missing', message='Classifier file is missing.Please contact me for help :/')

def getImagesAndLabels(path):
    # get the path of all the files in the folder
    imagePaths = [os.path.join(path, f) for f in os.listdir(path)]
    # create empty face list
    faces = []
    # create empty ID list
    Ids = []
    # now looping through all the image paths and loading the Ids and the images
    for imagePath in imagePaths:
        # loading the image and converting it to gray scale
        pilImage = Image.open(imagePath).convert('L')
        # Now we are converting the PIL image into numpy array
        imageNp = np.array(pilImage, 'uint8')
        # getting the Id from the image
        ID = int(os.path.split(imagePath)[-1].split(".")[1])
        # extract the face from the training image sample
        faces.append(imageNp)
        Ids.append(ID)
    return faces, Ids


class MainApp(tk.Tk):
    def __init__(self, *args, **kwargs):
        tk.Tk.__init__(self, *args, **kwargs)

        container = Frame(self)
        container.pack(side="top", fill="both", expand=True)

        container.grid_rowconfigure(0, weight=1)
        container.grid_columnconfigure(0, weight=1)

        self.frames = {}

        for fr in (StartPage, AddUser, RollCall):
            frame = fr(container, self)

            self.frames[fr] = frame
            frame.grid(row=0, column=0, sticky="nsew")

        self.show_frame(StartPage)

    def show_frame(self, page):
        frame = self.frames[page]
        frame.tkraise()
        self.title("UNIVERSITY ATTENDANCE APPLICATION")
        self.iconbitmap("rec.ico")
        self.configure(background='blue')

class StartPage(Frame):

    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        # sidebar = Frame(self, width=100, bg='dark slate blue', height=700, relief='sunken', borderwidth=2)
        # sidebar.pack(expand=True, fill='both', side='left', anchor='nw')
        #
        # mainarea = Frame(self, width=1200, height=700)
        # mainarea.pack(expand=True, fill='both', side='right')

        bg = Image.open('backg2.gif')
        bgimg = ImageTk.PhotoImage(bg)
        imglbl = Label(self, image=bgimg)
        imglbl.img = bgimg
        imglbl.place(x=0, y=0)

        message = Label(self, text="Face-Recognition Attendance Application ", bg='midnight blue', fg='white', width=60,
                        height=2, font=('times', 30, 'bold'), justify="left")
        message.place(x=0, y=0)

        message = Label(self, text="                           ", bg="midnight blue", width=14, height=60)
        message.place(x=1260, y=0)

        canvas = Canvas(self)
        canvas.place(x=20, y=100,width=400, height=80)
        canvas_t = canvas.create_text(10,10,text='',font =('cursive',13,'bold','italic'),anchor=NW)
        welcometxt = "Welcome to the face recognition attendance app.\n\nPlease find out more from the 'About' option."
        delta = 100
        delay = 0
        for x in range(len(welcometxt)+1):
            s = welcometxt[:x]
            new_text = lambda s=s: canvas.itemconfigure(canvas_t,text=s)
            canvas.after(delay,new_text)
            delay += delta

        Addbttn = Button(self, text="Add User",activebackground = 'LightGoldenrod1', command=lambda: controller.show_frame(AddUser))
        Addbttn.place(x=390, y=210, width=300, height=70)

        Rollbttn = Button(self, text="Roll-Call",activebackground = 'LightGoldenrod1', command=lambda: controller.show_frame(RollCall))
        Rollbttn.place(x=390, y=320, width=300, height=70)

        Quitbttn = Button(self, text="Quit", activebackground = 'LightGoldenrod1', command = self.quit)
        Quitbttn.place(x=390, y=430, width=300, height=70)

class AddUser(Frame):
    def __init__(self, parent, controller):
        Frame.__init__(self, parent)

        bg = Image.open('backg2.gif')
        bgimg = ImageTk.PhotoImage(bg)
        imglbl = Label(self, image=bgimg)
        imglbl.img = bgimg
        imglbl.place(x=50, y=0)

        self.label = Label(self, text="ADD NEW USER", bg='midnight blue', fg='white', width=60, height=2,
                           font=('times', 30, 'bold'), justify="left")
        self.label.place(x=0, y=0)

        l2 = Label(self, text="USER DETAILS", font=('Algerian', 24, 'bold'), fg='black')
        l2.place(x=150, y=160)

        t1 = Label(self, text="Name:", font=('times', 17, 'bold'))
        t1.place(x=150, y=230)
        self.name_entry = Entry(self, width=70, bd=5)
        self.name_entry.place(x=150, y=260)
        self.name_entry.focus()

        l4 = Label(self, text="Index No:", font=('times', 17, 'bold'))
        l4.place(x=150, y=310)
        self.index_entry = Entry(self, width=70, bd=5)
        self.index_entry.place(x=150, y=340)

        l5 = Label(self, text="Reference ID:", font=('times', 17, 'bold'))
        l5.place(x=150, y=410)
        self.ref_entry = Entry(self, width=70, bd=5)
        self.ref_entry.place(x=150, y=440)

        takebtn = Button(self, text="Take",activebackground = 'LightGoldenrod1', command=self.TakeImages)
        takebtn.place(x=150, y=500, width=100, height=70)

        trainbbtn = Button(self, text='Train',activebackground = 'LightGoldenrod1', command=self.TrainImages)
        trainbbtn.place(x=300, y=500, width=100, height=70)

        confirmbttn = Button(self, text = 'Confirm Save',activebackground = 'LightGoldenrod1', command=self.ConfirmSave)
        confirmbttn.place(x=420, y=500, width=150, height = 70)

        homebttn = Button(self, text="Back", activebackground = 'LightGoldenrod1',command = lambda: controller.show_frame(StartPage))
        homebttn.place(x=600, y=500, width=100, height=70)

    def TakeImages(self):
        check_haarcascadefile()
        columns = ['SERIAL', '', 'INDEX', '', 'NAME','', 'REFERENCE']
        assure_path_exists("StudentFile/")
        assure_path_exists("FaceData/")
        self.serial = 0
        exists = os.path.isfile("StudentFile\StudentData.csv")
        if exists:
            with open("StudentFile\StudentData.csv", 'r') as csvFile1:
                reader1 = csv.reader(csvFile1)
                for l in reader1:
                    self.serial = self.serial + 1
            self.serial = (self.serial // 2)
            csvFile1.close()
        else:
            with open("StudentFile\StudentData.csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(columns)
                self.serial = 1
            csvFile1.close()
        Index = (self.index_entry.get())
        name = (self.name_entry.get())
        reference =(self.ref_entry.get())

        if ((name.isalpha()) or (' ' in name)):
            cam = cv2.VideoCapture(0, cv2.CAP_MSMF)
            harcascadePath = "haarcascade_frontalface_default.xml"
            detector = cv2.CascadeClassifier(harcascadePath)
            sampleNum = 0
            while (True):
                ret, img = cam.read()
                gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
                faces = detector.detectMultiScale(gray, 1.05, 5)
                for (x, y, w, h) in faces:
                    cv2.rectangle(img, (x, y), (x + w, y + h), (0, 255, 0), 2)
                    # incrementing sample number
                    sampleNum = sampleNum + 1
                    # saving the captured face in the dataset folder TrainingImage
                    cv2.imwrite("FaceData\ " + name + "." + str(self.serial) + "." + Index + '.' + str(sampleNum) + ".jpg",
                                gray[y:y + h, x:x + w])
                    # display the frame
                    cv2.imshow('Taking Images', img)
                    cv2.putText(img, "Please press 'q' to close webcam", (10, 40), cv2.FONT_HERSHEY_PLAIN, 1,
                                (0, 0, 225), 1)
                # wait for 100 miliseconds
                if cv2.waitKey(100) & 0xFF == ord('q'):
                    break
                # break if the sample number is morethan 100
                elif sampleNum > 100:
                    break
            cam.release()
            cv2.destroyAllWindows()
            res = "Images Taken for Student : " + name + '\n' + "Index : " + Index
            row = [self.serial, '', Index, '', name, '', reference]
            with open('StudentFile\StudentData.csv', 'a+') as csvFile:
                writer = csv.writer(csvFile)
                writer.writerow(row)
            csvFile.close()
            self.label.configure(text=res)
        else:
            if (name.isalpha() == False) or (len(self.name_entry.get()==0)):
                res = "Enter Correct name"
                self.label.configure(text=res)
            if (Index.isnumeric() == False) or (len(self.index_entry.get()==0)):
                res = "Enter the index number"
            if (reference.isnumeric() == False) or (len(self.ref_entry.get()==0)):
                res = "Enter reference number"

    def TrainImages(self):
        check_haarcascadefile()
        assure_path_exists("labels/")
        recognizer = cv2.face_LBPHFaceRecognizer.create()
        harcascadePath = "haarcascade_frontalface_default.xml"
        detector = cv2.CascadeClassifier(harcascadePath)
        faces, ID = getImagesAndLabels("FaceData")
        try:
            recognizer.train(faces, np.array(ID))
        except:
            mess._show(title='No Registrations', message='Please Register someone first!!!')
            return
        recognizer.save("labels\Trainner.yml")
        res = "Student Profile Saved Successfully \n Total Registrations till now  : " + str(ID[0])
        self.label.configure(text=res)

    def ConfirmSave(self):
        check_haarcascadefile()
        assure_path_exists("RollCall/")
        assure_path_exists("StudentFile/")

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        exists3 = os.path.isfile("labels\Trainner.yml")
        if exists3:
            recognizer.read("labels\Trainner.yml")
        else:
            mess._show(title='Data Missing', message='Please click on Clear to reset data!!')
            return
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)

        cam = cv2.VideoCapture(0, cv2.CAP_MSMF)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Index', '', 'Name', '', 'Date', '', 'Time']
        exists1 = os.path.isfile("StudentFile\StudentData.csv")
        if exists1:
            df = pd.read_csv("StudentFile\StudentData.csv")
        else:
            mess._show(title='Details Missing', message='Students details are missing, please check!')
            cam.release()
            cv2.destroyAllWindows()
            self.destroy()
        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(im, "Please press 'q' to close webcam", (10, 40), cv2.FONT_HERSHEY_PLAIN, 1, (0, 0, 225),
                            1)
                self.serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if 'SERIAL' in df and (conf < 60):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['SERIAL'] == self.serial]['NAME'].values
                    ID = df.loc[df['SERIAL'] == self.serial]['INDEX'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                else:
                    Id = 'Unknown'
                    bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (0, 251, 255), 2)

            cv2.imshow('Taking Attendance', im)
            if (cv2.waitKey(1) == ord('q')):
                break

        cam.release()
        cv2.destroyAllWindows()


class RollCall(Frame):
    def __init__(self, parent, controller, video_source=0):
        Frame.__init__(self, parent)

        bg = Image.open('backimg2.gif')
        bgimg = ImageTk.PhotoImage(bg)
        imglbl = Label(self, image=bgimg)
        imglbl.img = bgimg
        imglbl.place(x=0, y=0)

        self.label = Label(self, text="STUDENT ATTENDANCE RECORD", bg='midnight blue', fg='white', width=60, height=2,
                           font=('times', 30, 'bold'), justify="left")
        self.label.place(x=0, y=0)

        total = Label(self, text=" ", fg='black',
                           font=('calibri', 17, 'bold'), justify="left")
        total.place(x=230, y=140)

        self.style = ttk.Style()
        self.style.configure("mystyle.Treeview", highlightthickness=0, bd=0,
                        font=('Calibri', 11))  # Modify the font of the body
        self.style.configure("mystyle.Treeview.Heading", font=('times', 13, 'bold'))
        self.table = ttk.Treeview(self,height =17,style="mystyle.Treeview")
        self.table['columns']= ('Name','Date','Time')
        self.table.column('#0', width = 140)
        self.table.column('Name', width = 330)
        self.table.column('Date', width = 190)
        self.table.column('Time',  width = 190)

        self.table.heading('#0', text='INDEX', anchor=CENTER)
        self.table.heading('Name', text= 'NAME',anchor = CENTER)
        self.table.heading('Date',text='DATE', anchor = CENTER)
        self.table.heading('Time', text='TIME', anchor= CENTER)
        self.table.grid(row=2, column=0, padx=(210,0), pady=(200,0),columnspan=4)

        self.treeview = self.table
        res = " Total number of students recorded : " + str(len(self.table.get_children()))
        total.configure(text=res)

        backbttn = Button(self, text='Back', activebackground = 'LightGoldenrod1',command= lambda : controller.show_frame(StartPage))
        backbttn.place(x=220, y=590, width=100, height=70)

        openbttn = Button(self, text='Data', activebackground = 'LightGoldenrod1',command = self.data)
        openbttn.place(x=370, y=590, width=100, height=70)

        attdbttn = Button(self, text='Take Attendance',activebackground = 'LightGoldenrod1', command = self.TrackImages)
        attdbttn.place(x=500, y=590, width=200, height=70)

        clearbtn = Button(self, text = 'Clear',activebackground = 'LightGoldenrod1', command = self.clear)
        clearbtn.place(x=740, y=590, width=100, height=70)

    def clear(self):
        self.table.delete(*self.table.get_children())

    def data(self):
        directory = filedialog.askdirectory(initialdir = os.path.normpath("C://"), title = "Open Attendance Data")

    def TrackImages(self):
        check_haarcascadefile()
        assure_path_exists("RollCall/")
        assure_path_exists("StudentFile/")

        for k in self.table.get_children():
            self.table.delete(k)
        msg = ''
        i = 0
        j = 0

        recognizer = cv2.face.LBPHFaceRecognizer_create()
        exists3 = os.path.isfile("labels\Trainner.yml")
        if exists3:
            recognizer.read("labels\Trainner.yml")
        else:
            mess._show(title='Data Missing', message='Please click on Clear to reset data!!')
            return
        harcascadePath = "haarcascade_frontalface_default.xml"
        faceCascade = cv2.CascadeClassifier(harcascadePath)

        cam = cv2.VideoCapture(0, cv2.CAP_MSMF)
        font = cv2.FONT_HERSHEY_SIMPLEX
        col_names = ['Index', '', 'Name', '', 'Date', '', 'Time']
        exists1 = os.path.isfile("StudentFile\StudentData.csv")
        if exists1:
            df = pd.read_csv("StudentFile\StudentData.csv")
        else:
            mess._show(title='Details Missing', message='Students details are missing, please check!')
            cam.release()
            cv2.destroyAllWindows()
            self.destroy()
        while True:
            ret, im = cam.read()
            gray = cv2.cvtColor(im, cv2.COLOR_BGR2GRAY)
            faces = faceCascade.detectMultiScale(gray, 1.2, 5)
            for (x, y, w, h) in faces:
                cv2.rectangle(im, (x, y), (x + w, y + h), (255, 0, 0), 2)
                cv2.putText(im, "Please press 'q' to close webcam", (10, 40), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 225),
                            2)
                self.serial, conf = recognizer.predict(gray[y:y + h, x:x + w])
                if 'SERIAL' in df and (conf < 60):
                    ts = time.time()
                    date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
                    timeStamp = datetime.datetime.fromtimestamp(ts).strftime('%H:%M:%S')
                    aa = df.loc[df['SERIAL'] == self.serial]['NAME'].values
                    ID = df.loc[df['SERIAL'] == self.serial]['INDEX'].values
                    ID = str(ID)
                    ID = ID[1:-1]
                    bb = str(aa)
                    bb = bb[2:-2]
                    attendance = [str(ID), '', bb, '', date, '', str(timeStamp)]

                else:
                    Id = 'Unknown'
                    bb = str(Id)
                cv2.putText(im, str(bb), (x, y + h), font, 1, (0, 251, 255), 2)

            cv2.imshow('Taking Attendance', im)

            if (cv2.waitKey(1) == ord('q')):
                break
        ts = time.time()
        date = datetime.datetime.fromtimestamp(ts).strftime('%d-%m-%Y')
        exists = os.path.isfile("RollCall\Attendance_" + date + ".csv")
        if exists:
            with open("RollCall\Attendance_" + date + ".csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(attendance)
            csvFile1.close()
        else:
            with open("RollCall\Attendance_" + date + ".csv", 'a+') as csvFile1:
                writer = csv.writer(csvFile1)
                writer.writerow(col_names)
                writer.writerow(attendance)
            csvFile1.close()
        with open("RollCall\Attendance_" + date + ".csv", 'r') as csvFile1:
            reader1 = csv.reader(csvFile1)
            for lines in reader1:
                i = i + 1
                if (i > 1):
                    if (i % 2 != 0):
                        iidd = str(lines[0]) + '   '
                        self.table.insert('', 0, text=iidd, values=(str(lines[2]), str(lines[4]), str(lines[6])))
        csvFile1.close()
        cam.release()
        cv2.destroyAllWindows()


app = MainApp()

#close
def on_closing():
    if mess.askyesno("Quit", "You are exiting window.Do you want to quit?"):
        app.destroy()

#contact
def contact():
    mess._show(title="Contact Me",
                message="If you need any help or have any enquiries, this is my number please;0208226180")

    # about
def about():
    mess._show(title="About",
                message='To register a new user,first take images and save profile \n Then click confirm save to check if user data has been stored\n\n On the RollCall page, Data opens a find file directory so that you can locate the attendance CSV file')


menubar=Menu(app)
help=Menu(menubar,tearoff=0)
help.add_command(label="Contact Us",command=contact)
help.add_separator()
help.add_command(label="Exit",command=on_closing)
menubar.add_cascade(label="Help",menu=help)

# add ABOUT label to menubar-------------------------------
menubar.add_command(label="About",command=about)
app.config(menu=menubar)


#app window configuration
# app.resizable(True,True)
# app.attributes("-fullscreen", True)
# app.bind("<F11>", lambda event: app.attributes("-fullscreen",not app.attributes("-fullscreen")))
# app.bind("<Escape>", lambda event: app.attributes("-fullscreen", False))

w = 1280
h = 720
ws = app.winfo_screenwidth()
hs = app.winfo_screenheight()

x = (ws/2) - (w/2)
y = (hs/2) - (h/2)
app.geometry('%dx%d+%d+%d' % (w, h, x, y))

app.protocol("WM_DELETE_WINDOW", on_closing)
app.mainloop()




































# end of code
