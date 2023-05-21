import cv2
import time
from os import mkdir
import win32gui
import win32con
from tkinter import Tk, Button, filedialog

# Creating a constant for the window title
WINDOW_TITLE = "CCTV camera"

# ===============================================
try:
    mkdir('footages')
except FileExistsError:
    pass

# Method to add minimize feature
def minimizeWindow():
    # Get the handle of the foreground window
    window = win32gui.GetForegroundWindow()
    # Minimize the window
    win32gui.ShowWindow(window, win32con.SW_MINIMIZE)

# Video Camera
def cctv():
    video = cv2.VideoCapture(0)
    video.set(3, 640)
    video.set(4, 480)
    width = video.get(3)
    height = video.get(4)
    print("Video resolution is set to:", width, "X", height)
    print("--Help:\n1. Press Esc key to exit CCTV.\n2. Press M to minimize window.")

    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    date_time = time.strftime("recording %H-%M -%d %m %y")
    output = cv2.VideoWriter('footages/' + date_time + '.mp4', fourcc, 20.0, (640, 480))

    while video.isOpened():
        check, frame = video.read()
        if check:
            frame = cv2.flip(frame, 1)

            t = time.ctime()
            cv2.rectangle(frame, (5, 5, 100, 20), (255, 255, 255), cv2.FILLED)
            cv2.putText(frame, "Camera 1", (20, 20), cv2.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 2)
            cv2.putText(frame, t, (420, 460), cv2.FONT_HERSHEY_DUPLEX, 0.5, (5, 5, 5), 1)

            cv2.imshow(WINDOW_TITLE, frame)
            output.write(frame)

            key = cv2.waitKey(1)
            if key == 27:  # Esc key
                print("Video footage saved in current directory.\nBe safe & secure!")
                break
            elif key == ord('m') or key == ord('M'):
                minimizeWindow()

        else:
            print("Can't open this camera. Select another or check its configuration.")
            break

    video.release()
    output.release()
    cv2.destroyAllWindows()

# Function to save the recorded file
def saveFile():
    root = Tk()
    root.withdraw()
    file_path = filedialog.asksaveasfilename(defaultextension=".mp4",
                                             filetypes=(("MP4 files", "*.mp4"), ("All files", "*.*")))
    if file_path:
        # Rename the recorded file with the selected file path
        current_date_time = time.strftime("%H-%M -%d %m %y")
        new_file_path = file_path + "_" + current_date_time + ".mp4"
        try:
            # Rename the file
            os.rename("footages/recording.mp4", new_file_path)
            print("Video footage saved as:", new_file_path)
        except FileNotFoundError:
            print("No recorded file found.")

# Now it's time to run the app
print("*" * 80 + "\n" + " " * 30 + "Welcome to CCTV software\n" + "*" * 80)

while True:
    ask = input('Do you want to start CCTV?\n1. Yes\n2. No\n>>> ').lower()

    if ask == '1' or ask == 'yes':
        cctv()
        break
    elif ask == '2' or ask == 'no':
        print("Bye bye! Be safe & secure!")
        break
    else:
        print("Invalid choice. Please enter 1/Yes or 2/No.")

    if ask == '1' or ask == 'yes':
        saveFile()
