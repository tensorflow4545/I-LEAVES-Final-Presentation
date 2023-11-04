import numpy as np
import cv2
from collections import deque
import datetime
# default called trackbar function
def setValues(x):
    print("")
# Creating the trackbars needed for adjusting the marker colour These trackbars will be used for setting the upper and lower ranges of the HSV required for particular colour
cv2.namedWindow("Color detectors")
cv2.createTrackbar("Upper Hue", "Color detectors",
                   200, 20, setValues)
cv2.createTrackbar("Upper Saturation", "Color detectors",
                   255, 255, setValues)
cv2.createTrackbar("Upper Value", "Color detectors",
                   255, 255, setValues)
cv2.createTrackbar("Lower Hue", "Color detectors",
                   64, 180, setValues)
cv2.createTrackbar("Lower Saturation", "Color detectors",
                   72, 255, setValues)
cv2.createTrackbar("Lower Value", "Color detectors",
                   215, 255, setValues)
#mine
# cv2.createTrackbar("Lower Value for Blue", "Color detectors", 150, 200, setValues)

# Giving different arrays to handle colour points of different colour These arrays will hold the points of a particular colour in the array which will further be used to draw on canvas
blue_points = [deque(maxlen=1024)]  #range of working
red_points = [deque(maxlen=1024)]
black_points = [deque(maxlen=1024)]
Erase_Point=[deque(maxlen=1024)]
upload_points=[deque(maxlen=1024)]
calculator_points = [deque(maxlen=1024)]

# These indexes will be used to mark position of pointers in colour array
blue_index = 0
black_index = 0
red_index = 0
erase_index=0
upload_points=0
calculator_index = 0
# The kernel to be used for dilation purpose
kernel = np.ones((2, 2), np.uint8)           #detect the distance of cursor and cammera ,less better
# The colours which will be used as ink for the drawing purpose
colors = [(255, 0, 0), (0,0, 0), (0, 0, 255), (0, 255, 255), (255, 0, 255),(255,255,255)] #implement white
colorIndex = 0
Paint = np.zeros((700, 1600, 3)) + 255

# Here is code for Canvas setup
paintWindow = np.zeros((471, 636, 3)) + 255  #all for paint height/length/rgb ,space color
# Loading the default webcam of PC.
cap = cv2.VideoCapture(1)
count = 0
# Keep looping
while True:
    # Reading the frame from the camera
    ret, frame = cap.read()

    # Flipping the frame to see same side of yours
    frame = cv2.flip(frame, 1)
    hsv = cv2.cvtColor(frame, cv2.COLOR_BGR2HSV)

    # Getting the updated positions of the trackbar and setting the HSV valuespython -m venv venv
    u_hue = cv2.getTrackbarPos("Upper Hue","Color detectors")
    u_saturation = cv2.getTrackbarPos("Upper Saturation","Color detectors")
    u_value = cv2.getTrackbarPos("Upper Value","Color detectors")
    l_hue = cv2.getTrackbarPos("Lower Hue","Color detectors")
    l_saturation = cv2.getTrackbarPos("Lower Saturation","Color detectors")
    l_value = cv2.getTrackbarPos("Lower Value","Color detectors")

    Upper_hsv = np.array([u_hue, u_saturation, u_value])
    Lower_hsv = np.array([l_hue, l_saturation, l_value])
    # Adding the colour buttons to the live frame for BOX colour Adding the colour buttons to the live frame for BOX colour
    frame = cv2.rectangle(frame, (0, 0), (80, 55), (122, 80, 150), -1)  # box space and color contrast
    frame = cv2.rectangle(frame, (90, 0), (150, 30), colors[0], -1)
    frame = cv2.rectangle(frame, (160, 0), (240, 30), colors[1], -1)
    frame = cv2.rectangle(frame, (250, 0), (310, 30), colors[2], -1)
    frame = cv2.rectangle(frame, (320, 0), (400, 30), colors[3], -1)
     # Calculator and Eraser and Undo
    frame = cv2.rectangle(frame, (410, 0), (530, 30), (200, 200, 0), -1)  # Calculator
    frame = cv2.rectangle(frame, (540, 0), (650, 30), (255, 255, 255), -1)  # eraser

    # Text on buttons
    cv2.putText(frame, "CLEAR ALL", (0, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, "BLUE", (100, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, "BLACK", (180, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 100, 100), 1, cv2.LINE_AA)
    cv2.putText(frame, "RED", (260, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (255, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, "UPLOAD", (340, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (100, 100, 100), 1, cv2.LINE_AA)
    cv2.putText(frame, "CALCULATOR", (420, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (200, 255, 255), 1, cv2.LINE_AA)
    cv2.putText(frame, "ERASER", (570, 20), cv2.FONT_HERSHEY_SIMPLEX, 0.45, (0, 0, 0), 1,cv2.LINE_AA)  # adjusted to fit properly

    frame = cv2.rectangle(frame, (0, 56), (700, 57),colors[3], -1)
    # Identifying the pointer by making its

    Mask = cv2.inRange(hsv, Lower_hsv, Upper_hsv)
    Mask = cv2.erode(Mask, kernel, iterations=1)
    Mask = cv2.morphologyEx(Mask, cv2.MORPH_OPEN, kernel)
    Mask = cv2.dilate(Mask, kernel, iterations=1)

    # Find contours for the pointer after identifying it
    cnts, _ = cv2.findContours(Mask.copy(), cv2.RETR_EXTERNAL,
                               cv2.CHAIN_APPROX_SIMPLE)
    center = None

    # Ifthe contours are formed
    if len(cnts) > 0:       #cursor range of detection

        # sorting the contours to find biggest
        cnt = sorted(cnts, key=cv2.contourArea, reverse=True)[0]
        # Get the radius of the enclosing circle around the found contour
        ((x, y), radius) = cv2.minEnclosingCircle(cnt)

        # Draw the circle around the contour
                                 #all for cursor 👆
        cv2.circle(frame, (int(x), int(y)), int(radius), (0, 255, 255), 1) #yellow,circle purotto

        # Calculating the center of the detected contour
        M = cv2.moments(cnt)
        try:
            center = (int(M['m10'] / M['m00']), int(M['m01'] / M['m00']))
        except (ZeroDivisionError, KeyError) as e:
            # Handle the ZeroDivisionError and KeyError exceptions here
            print(f"An error occurred: {e}")

        # Now checking if the user wants to click on any button above the screen
        if center[1] <= 60: #detect range⬇

            # Clear Button
            if 00 <= center[0] <= 100:  # clear range 0-100
                blue_points= [deque(maxlen=512)]
                black_points = [deque(maxlen=512)]
                red_points = [deque(maxlen=512)]
                upload_points = [deque(maxlen=512)]
                calculator_points = [deque(maxlen=512)]  # mine white
                Erase_Point =[deque(maxlen=512)]

                blue_index = 0
                black_index = 0
                red_index = 0
                catalog_index = 0
                catalog_index = 0
                erase_index=0

                # paintWindow[67:, :, :] = 255

            if 410 <= center[0] <= 510: #clear range 0-100

                # import everything from the tkinter module
                from tkinter import *
                # message when there is some error
                import tkinter.messagebox
                # import math functions
                import math

                # Initializing the main window(container)
                root = Tk()
                # assigning our main window a size
                root.geometry("650x400+300+300")
                # assigning our main a window a title
                root.title("Scientific Calculator")

                switch = None
                # Button on press

                # display of 1
                def btn1_clicked():
                    # if only 0 is written on the screen
                    if disp.get() == '0':
                        # delete all the expression on the screen
                        disp.delete(0, END)
                    # length of the expression written on the screen
                    pos = len(disp.get())
                    # written the 1 after the pos
                    # for example
                    # if we click 2 2 1
                    # then the number display in screen is 221
                    disp.insert(pos, '1')
                    # else if we write disp.insert(0, '1')
                    # then if we click 2 2 1
                    # then the number display in screen is 122


                # display of 2
                def btn2_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '2')


                # display of 3
                def btn3_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '3')


                # display of 4
                def btn4_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '4')


                # display of 5
                def btn5_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '5')


                # display of 6
                def btn6_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '6')


                # display of 7
                def btn7_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '7')


                # display of 8
                def btn8_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '8')


                # display of 9
                def btn9_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '9')


                # display of 0
                def btn0_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, '0')


                def key_event(*args):
                    if disp.get() == '0':
                        disp.delete(0, END)


                # addition operator
                def btnp_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, '+')


                # substract operator
                def btnm_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, '-')


                # multiplication operator
                def btnml_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, '*')


                # divide operator
                def btnd_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, '/')


                # delete all the input
                def btnc_clicked(*args):
                    disp.delete(0, END)
                    disp.insert(0, '0')


                # sin function
                def sin_clicked():
                    try:
                        ans = float(disp.get())
                        if switch is True:
                            ans = math.sin(math.radians(ans))
                        else:
                            ans = math.sin(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # cos function
                def cos_clicked():
                    try:
                        ans = float(disp.get())
                        if switch is True:
                            ans = math.cos(math.radians(ans))
                        else:
                            ans = math.cos(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # tan function
                def tan_clicked():
                    try:
                        ans = float(disp.get())
                        if switch is True:
                            ans = math.tan(math.radians(ans))
                        else:
                            ans = math.tan(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # arcsin function
                def arcsin_clicked():
                    try:
                        ans = float(disp.get())
                        if switch is True:
                            ans = math.degrees(math.asin(ans))
                        else:
                            ans = math.asin(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # arccos function
                def arccos_clicked():
                    try:
                        ans = float(disp.get())
                        if switch is True:
                            ans = math.degrees(math.acos(ans))
                        else:
                            ans = math.acos(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # arctan function
                def arctan_clicked():
                    try:
                        ans = float(disp.get())
                        if switch is True:
                            ans = math.degrees(math.atan(ans))
                        else:
                            ans = math.atan(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # power function
                def pow_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, '**')


                # round function
                def round_clicked():
                    try:
                        ans = float(disp.get())
                        ans = round(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # logarithm function with base 10
                def logarithm_clicked():
                    try:
                        ans = float(disp.get())
                        ans = math.log10(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # factorial function
                def fact_clicked():
                    try:
                        ans = float(disp.get())
                        ans = math.factorial  # (ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # square root function
                def sqr_clicked():
                    try:
                        ans = float(disp.get())
                        ans = math.sqrt(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # dot operator
                def dot_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, '.')


                # pie operator
                def pi_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, str(math.pi))


                # exponential function
                def e_clicked():
                    if disp.get() == '0':
                        disp.delete(0, END)
                    pos = len(disp.get())
                    disp.insert(pos, str(math.e))


                # ( operator
                def bl_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, '(')


                # ) operator
                def br_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, ')')


                # deleting the number or operator
                def del_clicked():
                    pos = len(disp.get())
                    display = str(disp.get())
                    if display == '':
                        disp.insert(0, '0')
                    elif display == ' ':
                        disp.insert(0, '0')
                    elif display == '0':
                        pass
                    else:
                        disp.delete(0, END)
                        disp.insert(0, display[0:pos - 1])


                # conversion of degree to rad
                def conv_clicked():
                    global switch
                    if switch is None:
                        switch = True
                        conv_btn['text'] = "Deg"
                    else:
                        switch = None
                        conv_btn['text'] = "Rad"


                # logorithm function with base e
                def ln_clicked():
                    try:
                        ans = float(disp.get())
                        ans = math.log(ans)
                        disp.delete(0, END)
                        disp.insert(0, str(ans))
                    except Exception:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # modulus fuction
                def mod_clicked():
                    pos = len(disp.get())
                    disp.insert(pos, '%')


                # evaluate answer equal operator
                def btneq_clicked(*args):
                    try:
                        # it is used to takes the takes the expression writen in screen
                        # here we take in variable ans
                        ans = disp.get()
                        # The eval() method parses the expression passed to it and runs python expression(code) within the program.
                        ans = eval(ans)
                        # it deletes all the expression writen on screen
                        disp.delete(0, END)
                        # it writes the value on the screen what value we writen
                        disp.insert(0, ans)

                    except:
                        tkinter.messagebox.showerror("Value Error", "Check your values and operators")


                # Label
                # data in string
                # Entry is used It is used to input the single line text entry from the user
                disp = Entry(root, font="Verdana 20", fg="black", bg="#abbab1", bd=0, justify=RIGHT,
                             insertbackground="#abbab1", cursor="arrow")
                # Tkinter bind is defined as a function for dealing with the functions and methods of Python that are bind to the events that occur during the program execution such as moving the cursor using a mouse, clicking of mouse buttons, clicking of buttons on the keyboard, etc are events that are handled using bind function in Tkinter.
                # widget.bind(event, handler)
                # whenever the enter key is pressed
                # then call the btneq_clicked function
                disp.bind("<Return>", btneq_clicked)
                # whenever the enter key is pressed
                # then call the btnc_clicked function
                disp.bind("<Escape>", btnc_clicked)
                disp.bind("<Key-1>", key_event)
                disp.bind("<Key-2>", key_event)
                disp.bind("<Key-3>", key_event)
                disp.bind("<Key-4>", key_event)
                disp.bind("<Key-5>", key_event)
                disp.bind("<Key-6>", key_event)
                disp.bind("<Key-7>", key_event)
                disp.bind("<Key-8>", key_event)
                disp.bind("<Key-9>", key_event)
                disp.bind("<Key-0>", key_event)
                disp.bind("<Key-.>", key_event)
                disp.insert(0, '0')
                # focus_set()=This method is used to set the focus on the desired widget if and only if the master window is focused.
                disp.focus_set()
                # pack organizes the widgets in blocks before placing in the parent widget.
                # expand according to the siz of window
                disp.pack(expand=TRUE, fill=BOTH)

                # Row 1 Buttons
                # frame acts as a container to hold the widgets. It is used for grouping and organizing the widgets.
                # syntax=Frame(master, option=value)
                btnrow1 = Frame(root, bg="#000000")
                # pack organizes the widgets in blocks before placing in the parent widget.
                btnrow1.pack(expand=TRUE, fill=BOTH)
                # To add a button in your application.
                # syntax = Button(master, option=value)
                pi_btn = Button(btnrow1, text="π", font="Segoe 18", relief=GROOVE, bd=0, command=pi_clicked, fg="white",
                                bg="#333333")
                pi_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                fact_btn = Button(btnrow1, text=" x! ", font="Segoe 18", relief=GROOVE, bd=0, command=fact_clicked,
                                  fg="white", bg="#333333")
                fact_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                sin_btn = Button(btnrow1, text="sin", font="Segoe 18", relief=GROOVE, bd=0, command=sin_clicked,
                                 fg="white", bg="#333333")
                sin_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                cos_btn = Button(btnrow1, text="cos", font="Segoe 18", relief=GROOVE, bd=0, command=cos_clicked,
                                 fg="white", bg="#333333")
                cos_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                tan_btn = Button(btnrow1, text="tan", font="Segoe 18", relief=GROOVE, bd=0, command=tan_clicked,
                                 fg="white", bg="#333333")
                tan_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn1 = Button(btnrow1, text="1", font="Segoe 23", relief=GROOVE, bd=0, command=btn1_clicked, fg="white",
                              bg="#333333")
                btn1.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn2 = Button(btnrow1, text="2", font="Segoe 23", relief=GROOVE, bd=0, command=btn2_clicked, fg="white",
                              bg="#333333")
                btn2.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn3 = Button(btnrow1, text="3", font="Segoe 23", relief=GROOVE, bd=0, command=btn3_clicked, fg="white",
                              bg="#333333")
                btn3.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btnp = Button(btnrow1, text="+", font="Segoe 23", relief=GROOVE, bd=0, command=btnp_clicked, fg="white",
                              bg="#333333")
                btnp.pack(side=LEFT, expand=TRUE, fill=BOTH)

                # Row 2 Buttons

                btnrow2 = Frame(root)
                btnrow2.pack(expand=TRUE, fill=BOTH)

                e_btn = Button(btnrow2, text="e", font="Segoe 18", relief=GROOVE, bd=0, command=e_clicked, fg="white",
                               bg="#333333")
                e_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                sqr_btn = Button(btnrow2, text=" √x ", font="Segoe 18", relief=GROOVE, bd=0, command=sqr_clicked,
                                 fg="white", bg="#333333")
                sqr_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                sinh_btn = Button(btnrow2, text="sin−1", font="Segoe 11 bold", relief=GROOVE, bd=0,
                                  command=arcsin_clicked, fg="white", bg="#333333")
                sinh_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                cosh_btn = Button(btnrow2, text="cos-1", font="Segoe 11 bold", relief=GROOVE, bd=0,
                                  command=arccos_clicked, fg="white", bg="#333333")
                cosh_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                tanh_btn = Button(btnrow2, text="tan-1", font="Segoe 11 bold", relief=GROOVE, bd=0,
                                  command=arctan_clicked, fg="white", bg="#333333")
                tanh_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn4 = Button(btnrow2, text="4", font="Segoe 23", relief=GROOVE, bd=0, command=btn4_clicked, fg="white",
                              bg="#333333")
                btn4.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn5 = Button(btnrow2, text="5", font="Segoe 23", relief=GROOVE, bd=0, command=btn5_clicked, fg="white",
                              bg="#333333")
                btn5.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn6 = Button(btnrow2, text="6", font="Segoe 23", relief=GROOVE, bd=0, command=btn6_clicked, fg="white",
                              bg="#333333")
                btn6.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btnm = Button(btnrow2, text="-", font="Segoe 23", relief=GROOVE, bd=0, command=btnm_clicked, fg="white",
                              bg="#333333")
                btnm.pack(side=LEFT, expand=TRUE, fill=BOTH)

                # Row 3 Buttons

                btnrow3 = Frame(root)
                btnrow3.pack(expand=TRUE, fill=BOTH)

                conv_btn = Button(btnrow3, text="Rad", font="Segoe 12 bold", relief=GROOVE, bd=0, command=conv_clicked,
                                  fg="white", bg="#333333")
                conv_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                round_btn = Button(btnrow3, text="round", font="Segoe 10 bold", relief=GROOVE, bd=0,
                                   command=round_clicked, fg="white", bg="#333333")
                round_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                ln_btn = Button(btnrow3, text="ln", font="Segoe 18", relief=GROOVE, bd=0, command=ln_clicked,
                                fg="white", bg="#333333")
                ln_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                logarithm_btn = Button(btnrow3, text="log", font="Segoe 17", relief=GROOVE, bd=0,
                                       command=logarithm_clicked, fg="white", bg="#333333")
                logarithm_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                pow_btn = Button(btnrow3, text="x^y", font="Segoe 17", relief=GROOVE, bd=0, command=pow_clicked,
                                 fg="white", bg="#333333")
                pow_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn7 = Button(btnrow3, text="7", font="Segoe 23", relief=GROOVE, bd=0, command=btn7_clicked, fg="white",
                              bg="#333333")
                btn7.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn8 = Button(btnrow3, text="8", font="Segoe 23", relief=GROOVE, bd=0, command=btn8_clicked, fg="white",
                              bg="#333333")
                btn8.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn9 = Button(btnrow3, text="9", font="Segoe 23", relief=GROOVE, bd=0, command=btn9_clicked, fg="white",
                              bg="#333333")
                btn9.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btnml = Button(btnrow3, text="*", font="Segoe 23", relief=GROOVE, bd=0, command=btnml_clicked,
                               fg="white", bg="#333333")
                btnml.pack(side=LEFT, expand=TRUE, fill=BOTH)

                # Row 4 Buttons

                btnrow4 = Frame(root)
                btnrow4.pack(expand=TRUE, fill=BOTH)

                mod_btn = Button(btnrow4, text="%", font="Segoe 21", relief=GROOVE, bd=0, command=mod_clicked,
                                 fg="white", bg="#333333")
                mod_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                bl_btn = Button(btnrow4, text=" ( ", font="Segoe 21", relief=GROOVE, bd=0, command=bl_clicked,
                                fg="white", bg="#333333")
                bl_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                br_btn = Button(btnrow4, text=" ) ", font="Segoe 21", relief=GROOVE, bd=0, command=br_clicked,
                                fg="white", bg="#333333")
                br_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                dot_btn = Button(btnrow4, text=" • ", font="Segoe 21", relief=GROOVE, bd=0, command=dot_clicked,
                                 fg="white", bg="#333333")
                dot_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btnc = Button(btnrow4, text="C", font="Segoe 23", relief=GROOVE, bd=0, command=btnc_clicked, fg="white",
                              bg="#333333")
                btnc.pack(side=LEFT, expand=TRUE, fill=BOTH)

                del_btn = Button(btnrow4, text="⌫", font="Segoe 20", relief=GROOVE, bd=0, command=del_clicked,
                                 fg="white", bg="#333333")
                del_btn.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btn0 = Button(btnrow4, text="0", font="Segoe 23", relief=GROOVE, bd=0, command=btn0_clicked, fg="white",
                              bg="#333333")
                btn0.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btneq = Button(btnrow4, text="=", font="Segoe 23", relief=GROOVE, bd=0, command=btneq_clicked,
                               fg="white", bg="#333333")
                btneq.pack(side=LEFT, expand=TRUE, fill=BOTH)

                btnd = Button(btnrow4, text="/", font="Segoe 23", relief=GROOVE, bd=0, command=btnd_clicked, fg="white",
                              bg="#333333")
                btnd.pack(side=LEFT, expand=TRUE, fill=BOTH)

                # running the application when application is ready to run
                root.mainloop()





            elif 110 <= center[0] <= 150:
                colorIndex = 0  # Blue

            elif 160 <= center[0] <= 250:
                colorIndex = 1  # black
            elif 260<= center[0] <= 310:
                colorIndex = 2  # Red
            elif 320 <= center[0] <= 400:

                count=count+1
                StrCount=str(count)
                current_date_time = datetime.datetime.now()
                cv2.imwrite('NotesNew '+StrCount+'.jpg', paintWindow)
                break
            elif 540 <= center[0] <= 650:
                colorIndex = 5

            frame = cv2.rectangle(frame, (0, 0), (80, 55), (122, 80, 150), -1)  # box space and color contrast
            frame = cv2.rectangle(frame, (90, 0), (150, 30), colors[0], -1)
            frame = cv2.rectangle(frame, (160, 0), (240, 30), colors[1], -1)
            frame = cv2.rectangle(frame, (250, 0), (310, 30), colors[2], -1)
            frame = cv2.rectangle(frame, (320, 0), (400, 30), colors[3], -1)

            # Calculator and Eraser
            frame = cv2.rectangle(frame, (410, 0), (530, 30), (200, 200, 0), -1)  # Calculator
            frame = cv2.rectangle(frame, (540, 0), (650, 30), (255, 255, 255), -1)  # eraser


        else:
            if colorIndex == 0:
                blue_points[blue_index].appendleft(center)
            elif colorIndex == 1:
                black_points[black_index].appendleft(center)
            elif colorIndex == 2:
                red_points[red_index].appendleft(center)
            elif colorIndex == 3:
                upload_points[catalog_index].appendleft(center)
            elif colorIndex == 4:
                calculator_points[purple_index].appendleft(center)
            elif colorIndex == 5:
                Erase_Point[erase_index].appendleft(center)

    # Append the next deques when nothing is
    # detected to avoid messing up
    else:
        blue_points.append(deque(maxlen=512))
        blue_index += 1
        black_points.append(deque(maxlen=512))
        black_index += 1
        red_points.append(deque(maxlen=512))
        red_index += 1

        calculator_points.append(deque(maxlen=512))
        calculator_index += 1
        Erase_Point.append(deque(maxlen=512))
        erase_index+=1

    # Draw lines of all the colors on the canvas and frame Function to switch to a particular color
    points = [blue_points, black_points, red_points, calculator_points,Erase_Point]
    for i in range(len(points)):

        for j in range(len(points[i])):

            for k in range(1, len(points[i][j])):

                if i == 4:  # If the color is the eraser (white)
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], (255, 255, 255), 20)  # Set as white
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], (255, 255, 255), 20)  # Set as white
                else:
                    cv2.line(frame, points[i][j][k - 1], points[i][j][k], colors[i], 2)  # Set as other colors
                    cv2.line(paintWindow, points[i][j][k - 1], points[i][j][k], colors[i], 2)  # Set as other colors
    # Show all the windows
    cv2.imshow("Tracking", frame)
    cv2.imshow("Paint", paintWindow)
    # If the 'q' key is pressed then stop the application
    if cv2.waitKey(1) & 0xFF == ord("q"):
        break
# Release the camera and all resources
cap.release()
cv2.destroyAllWindows()