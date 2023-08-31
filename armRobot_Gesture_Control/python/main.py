import serial
import cv2
import mediapipe as mp
import time
import tkinter as tk
from tkinter import PhotoImage
from tkinter import ttk

# config
write_video = True
debug = False
#cam_source = "http://192.168.1.100:4747/video" # 0,1 for usb cam, "http://192.168.1.165:4747/video" for webcam

#if not debug:
#if debug:
ser = None  # กำหนดให้ ser เป็น None ในกรณี debug mode
#else:
    #import serial
    #ser = serial.Serial('COM7', 115200)  # หรือใช้พอร์ตที่คุณต้องการ
   
def switch_to_subpage():
    main_frame.pack_forget()
    sub_frame.pack()

def switch_to_mainpage():
    sub_frame.pack_forget()
    main_frame.pack()

def switch_to_subpage1():
    main_frame.pack_forget()
    sub_frame1.pack()

def change_com_port():
    new_com_port = selected_com_port.get()  # Get the value from the Entry widget
    # Update the serial connection with the new COM port
    global ser
    if ser is not None:  # ตรวจสอบว่า ser ไม่เป็น None ก่อนที่จะเรียก close()
        ser.close()  # Close the current serial connection
    ser = serial.Serial(new_com_port, 115200)  # Open a new serial connection with the specified COM port
    update_com_port_label(new_com_port)  # Update the label text
    print(f"Serial port changed to {new_com_port}")

# Function to update the COM port label
def update_com_port_label(com_port):
    com_port_label.config(text=f"COM Port: {com_port} Changed DONE")



def switch_to_subpage1_popup():
    global subpage1_popup_open
    subpage1_popup_open = True

    sub_frame1_popup = tk.Toplevel(root)
    sub_frame1_popup.title("Mannual")
    sub_frame1_popup.geometry("650x600")

     # "Back" button aligned to the left side
    btn_back_sub1 = tk.Button(sub_frame1_popup, text="Back", command=sub_frame1_popup.destroy)
    btn_back_sub1.pack(pady=10,)



    canvas = tk.Canvas(sub_frame1_popup)
    canvas.pack(side=tk.LEFT, fill=tk.BOTH, expand=True)

    scrollbar = tk.Scrollbar(sub_frame1_popup, orient="vertical", command=canvas.yview)
    scrollbar.pack(side=tk.RIGHT, fill=tk.Y)

    canvas.configure(yscrollcommand=scrollbar.set)
    canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion=canvas.bbox("all")))

    frame_inside_canvas = tk.Frame(canvas)
    canvas.create_window((0, 0), window=frame_inside_canvas, anchor="nw")

    popup_text = """
        คู่มือการใช้งาน
        โปรแกรม Arm Robot Control เพื่อควบคุมหุ่นยนต์แขนกล

        1.ติดตั้งโปรแกรม เมื่อติดตั้งโปรแกรม Arm Robot Control สำเร็จแล้ว เปิดโปรแกรมเพื่อเริ่มใช้งาน
        2.เลือกพอร์ตการเชื่อมต่อ เชื่อมต่อหุ่นยนต์แขนกลเข้ากับคอมพิวเตอร์และเลือกพอร์ตการเชื่อมต่อ
        3.เลือกฟังก์ชันที่ต้องการ หน้าแรกของโปรแกรมจะมีฟังก์ชันการควบคุมอยู่ 2 รูปแบบ ได้แก่ Pattern Set Control 
        และ Gesture Control
        
        Pattern Set Control เป็นการควบคุมหุ่นยนต์แขนกลโดยชุดคำสั่งสำเร็จรูปสามารถใช้งานได้ทันที 
        โดยมีคำสั่งสำเร็จรูปจำนวน 4 ชุด ได้แก่
            A   หุ่นยนต์แขนกลจะคีบวัตถุจากทางด้านซ้ายสุดไปวางไว้ทางด้านขวาสุด
            B   หุ่นยนต์แขนกลจะคีบวัตถุจากทางด้านขวาสุดไปวางไว้ทางด้านซ้ายสุด
            C   หุ่นยนต์แขนกลจะคีบวัตถุขึ้นและวางลงตรงจุดเดิม
            D   หุ่นยนต์แขนกลจะขยับขึ้นลง ซ้ายขวา คีบปล่อย

                ข้อแนะนำ
        1.ตรวจสอบว่าอุปกรณ์ของคุณมีกล้องเว็บแคม
        2.หากตรวจพบว่ามีมือมากกว่า 1 มือ หุ่นยนต์แขนกลจะไม่ทำงาน
        3.ขณะทำการควบคุมควรให้ฝ่ามือตั้งฉากกับกล้องเว็บแคม และชูมือให้เห็นทั้ง 5 นิ้ว
        4.ปิดโปรแกรม เมื่อต้องการเลิกใช้งานโปรแกรมให้คลิกที่ไอคอน X ที่มุมขวาบน หรือ ESC เมื่ออยู๋ใน Gesture Control
    """

    popup_label = tk.Label(frame_inside_canvas, text=popup_text, justify="left")
    popup_label.pack(padx=20, pady=20)

    image_paths = ["gesture_MeArm-main/images/Forward.png",
                    "gesture_MeArm-main/images/back.png", 
                    "gesture_MeArm-main/images/top.png", 
                    "gesture_MeArm-main/images/down.png", 
                    "gesture_MeArm-main/images/left.png", 
                    "gesture_MeArm-main/images/right.png", 
                    "gesture_MeArm-main/images/gum.png", 
                    "gesture_MeArm-main/images/bea.png"]
    images = [PhotoImage(file=path).subsample(2) for path in image_paths]

    text_content = [
        "ขยับหน้า	ขยับมือเข้าไปใกล้กับกล้องเว็บแคม แขนของหุ่นยนต์แขนกลจะยื่นไปข้างหน้า",
        "ถอยหลัง	ขยับมือถอยห่างออกมาจากกล้องเว็บแคม แขนของหุ่นยนต์แขนกลจะหดถอย",
        "ยกสูง	ยกมือขึ้นสูง แขนของหุ่นยนต์แขนกลจะยกสูงขึ้น",
        "ลงต่ำ	ลดมือต่ำลง แขนของหุ่นยนต์แขนกลจะลดตัวลงต่ำ",
        "หมุนซ้าย	หมุนฝ่ามือไปทางซ้าย หุ่นยนต์แขนกลจะหมุนตัวไปทางซ้าย",
        "หมุนขวา	หมุนฝ่ามือไปทางขวา หุ่นยนต์แขนกลจะหมุนตัวไปทางขวา",
        "คีบ	กำมือเพื่อคีบวัตถุ",
        "ปล่อย	แบมือเพื่อปล่อยวัตถุ"
    ]

    for idx, image in enumerate(images):
        frame = tk.Frame(frame_inside_canvas)
        frame.pack(pady=10 ,padx=20, anchor="center")

        image_label = tk.Label(frame, image=image)
        image_label.image = image
        image_label.pack(pady=10, padx=20, anchor="center")  # Adding some padding

        text_label = tk.Label(frame, text=text_content[idx], wraplength=300, anchor="center", font=("Arial", 15))  # Adjust wrap length as needed
        text_label.pack(pady=5 ,padx=20 ,anchor="center")

    def on_canvas_mousewheel(event):
        canvas.yview_scroll(-1 * (event.delta // 120), "units")

    canvas.bind("<MouseWheel>", on_canvas_mousewheel)

def switch_to_mainpage1():
    global subpage1_popup_open
    subpage1_popup_open = False
    subpage1_popup.destroy()

# ... (previous code)

subpage1_popup_open = False
subpage1_popup = None  # เพิ่มบรรทัดนี้เพื่อประกาศตัวแปร subpage1_popup ให้สามารถใช้งานในทั้ง switch_to_subpage1_popup() และ switch_to_mainpage1()

   
def switch_to_subpage():
    main_frame.pack_forget()
    sub_frame.pack()

def switch_to_mainpage():
    sub_frame.pack_forget()
    main_frame.pack()

def send_arrayA():
    data = [102, 0, 165, 60,]  # ค่าอาเรย์ที่คุณต้องการส่ง
    data_bytes = bytearray(data)
    data1 = [102, 50, 165, 60,]
    data1_bytes = bytearray(data1)
    data2 = [35, 30, 130, 110,]
    data2_bytes = bytearray(data2)
    data3 = [35, 30, 131, 110,]
    data3_bytes = bytearray(data3)
    data4 = [35, 11, 171, 60,]
    data4_bytes = bytearray(data4)
    print("Pattern set : A ")
    ser.write(data_bytes)
    time.sleep(1) 
    ser.write(data1_bytes)
    time.sleep(1)
    ser.write(data2_bytes)
    time.sleep(1) 
    ser.write(data3_bytes)
    time.sleep(1)
    ser.write(data4_bytes)
    time.sleep(1)

def send_arrayB():
    data = [35, 0, 165, 60,]  # ค่าอาเรย์ที่คุณต้องการส่ง
    data_bytes = bytearray(data)
    data1 = [35, 50, 165, 60,]
    data1_bytes = bytearray(data1)
    data2 = [35, 30, 130, 110,]
    data2_bytes = bytearray(data2)
    data3 = [102, 30, 131, 110,]
    data3_bytes = bytearray(data3)
    data4 = [102, 11, 171, 60,]
    data4_bytes = bytearray(data4)
    print("Pattern set : B ")
    ser.write(data_bytes)
    time.sleep(1) 
    ser.write(data1_bytes)
    time.sleep(1)
    ser.write(data2_bytes)
    time.sleep(1) 
    ser.write(data3_bytes)
    time.sleep(1)
    ser.write(data4_bytes)
    time.sleep(1)


def send_arrayC():
    data = [75, 0, 145, 60,]  # ค่าอาเรย์ที่คุณต้องการส่ง
    data_bytes = bytearray(data)
    data1 = [75, 70, 180, 110,]
    data1_bytes = bytearray(data1)
    data2 = [75, 30, 130, 110,]
    data2_bytes = bytearray(data2)
    data3 = [75, 30, 131, 110,]
    data3_bytes = bytearray(data3)
    data4 = [75, 11, 171, 60,]
    data4_bytes = bytearray(data4)
    print("Pattern set : C ")
    ser.write(data_bytes)
    time.sleep(1) 
    ser.write(data1_bytes)
    time.sleep(1)
    ser.write(data2_bytes)
    time.sleep(1) 
    ser.write(data3_bytes)
    time.sleep(1)
    ser.write(data4_bytes)
    time.sleep(1)

def send_arrayD():
    data = [75, 0, 145, 60,]  # ค่าอาเรย์ที่คุณต้องการส่ง
    data_bytes = bytearray(data)
    data1 = [75, 100, 180, 110,]
    data1_bytes = bytearray(data1)
    data2 = [120, 30, 130, 110,]
    data2_bytes = bytearray(data2)
    data3 = [30, 30, 131, 110,]
    data3_bytes = bytearray(data3)
    data4 = [75, 11, 171, 60,]
    data4_bytes = bytearray(data4)
    print("Pattern set : D ")
    ser.write(data_bytes)
    time.sleep(1) 
    ser.write(data1_bytes)
    time.sleep(1)
    ser.write(data2_bytes)
    time.sleep(1) 
    ser.write(data3_bytes)
    time.sleep(1)
    ser.write(data4_bytes)
    time.sleep(1)


# สร้างหน้าต่างหลัก

root = tk.Tk()

root.title("Arm Robot Control")

root.iconphoto(False, tk.PhotoImage(file="gesture_MeArm-main/images/robotic-arm.png"))
# กำหนดขนาดของหน้าต่าง
root.geometry("400x300")

# สร้างเฟรมหลัก
main_frame = tk.Frame(root)
main_frame.pack(expand=True)

# เพิ่มตัวอักษร "PROJECT TTW" ตรงกลางหน้าต่าง
label = tk.Label(main_frame, text="Select Funchion", font=("Arial", 20))
label.pack(side=tk.TOP)

# ปรับปรุงปุ่มให้อยู่แนวนอน
button_frame = tk.Frame(main_frame)
button_frame.pack(pady=20)


# Create an Entry widget for the user to input the new COM port
#entry_com_port = tk.Entry(main_frame)
#entry_com_port.pack(pady=10)

# Create a StringVar to store the selected COM port
selected_com_port = tk.StringVar()
selected_com_port.set("Select COM port")  # Set the default value

# Create a OptionMenu (dropdown) to select the COM port
com_port_options = ["COM1", "COM2", "COM3", "COM4", "COM5","COM6", "COM7", "COM8", "COM9", "COM10", "COM11","COM12", "COM13", "COM14", "COM15", "COM16", "COM17", "COM18", "COM19", "COM20"]  # Add your COM port options here
com_port_combobox = ttk.Combobox(main_frame, textvariable=selected_com_port, values=com_port_options)
com_port_combobox.pack()

# Create a Button widget to trigger the COM port change
btn_change_com_port = tk.Button(main_frame, text="Change COM Port", command=change_com_port)
btn_change_com_port.pack()

# Create a Label to display the current COM port
current_com_port = 'Not Set' if ser is None else ser.port
com_port_label = tk.Label(main_frame, text=f"COM Port: {current_com_port}")
com_port_label.pack()

# สร้างปุ่ม "AutoPose" ที่เมื่อกดจะสลับไปยังหน้ารอง
btn_autopose = tk.Button(button_frame, text="Pattern set Control", command=switch_to_subpage)
btn_autopose.pack(side="left", padx=10)

# สร้างปุ่ม "Exit" ที่เมื่อกดจะปิดโปรแกรม
btn_exit = tk.Button(button_frame, text="Gesture control ", command=root.quit)
btn_exit.pack(side="left", padx=10)

#btn_switch_page = tk.Button(main_frame, text="Mannual", command=switch_to_subpage1)
#btn_switch_page.pack(pady=20)

btn_switch_page = tk.Button(main_frame, text="Please Read Me", command=switch_to_subpage1_popup)
btn_switch_page.pack(pady=20)


# ซ่อนเฟรมรองตอนเริ่มต้น
sub_frame = tk.Frame(root)


# สร้างปุ่ม A, B, C, D ในหน้ารอง
btn_a = tk.Button(sub_frame, text="A", command=send_arrayA)
btn_a.pack(pady=10)

btn_b = tk.Button(sub_frame, text="B", command=send_arrayB)
btn_b.pack(pady=10)

btn_a = tk.Button(sub_frame, text="C", command=send_arrayC)
btn_a.pack(pady=10)

btn_b = tk.Button(sub_frame, text="D", command=send_arrayD)
btn_b.pack(pady=10)



# สร้างปุ่ม "Back" เพื่อกลับไปยังหน้าหลัก
btn_back_sub = tk.Button(sub_frame, text="Back", command=switch_to_mainpage)
btn_back_sub.pack(pady=10)

# ซ่อนเฟรมรองตอนเริ่มต้น
sub_frame.pack_forget()

# สร้างเฟรมรองตอนเริ่มต้น
sub_frame1 = tk.Frame(root)

# สร้างปุ่ม "Back" เพื่อกลับไปยังหน้าหลัก
btn_back_sub1 = tk.Button(sub_frame1, text="Back", command=switch_to_mainpage1)
btn_back_sub1.pack(pady=10)

# ซ่อนเฟรมรองตอนเริ่มต้น
sub_frame1.pack_forget()

root.mainloop()

x_min = 15
x_mid = 75
x_max = 150
# use angle between wrist and index finger to control x axis
palm_angle_min = -60
palm_angle_mid = 20

y_min = 0
y_mid = 90
y_max = 180
# use wrist y to control y axis
wrist_y_min = 0.3    #0.3
wrist_y_max = 0.9     #0.9

z_min = 40 #10
z_mid = 90
z_max = 180
# use palm size to control z axis
plam_size_min = 0.1   #0.1
plam_size_max = 0.3   #0.3

claw_open_angle = 60
claw_close_angle = 120

servo_angle = [x_mid,y_mid,z_mid,claw_open_angle] # [x, y, z, claw]
prev_servo_angle = servo_angle
fist_threshold = 7

mp_drawing = mp.solutions.drawing_utils
mp_drawing_styles = mp.solutions.drawing_styles
mp_hands = mp.solutions.hands

cap = cv2.VideoCapture(0)
#####
# video writer
if write_video:
    fourcc = cv2.VideoWriter_fourcc(*'XVID')
    out = cv2.VideoWriter('output.avi', fourcc, 60.0, (640, 480))

clamp = lambda n, minn, maxn: max(min(maxn, n), minn)
map_range = lambda x, in_min, in_max, out_min, out_max: abs((x - in_min) * (out_max - out_min) // (in_max - in_min) + out_min)

# Check if the hand is a fist
def is_fist(hand_landmarks, palm_size):
    # calculate the distance between the wrist and the each finger tip
    distance_sum = 0
    WRIST = hand_landmarks.landmark[0]
    for i in [7,8,11,12,15,16,19,20]:
        distance_sum += ((WRIST.x - hand_landmarks.landmark[i].x)**2 + \
                         (WRIST.y - hand_landmarks.landmark[i].y)**2 + \
                         (WRIST.z - hand_landmarks.landmark[i].z)**2)**0.5
    return distance_sum/palm_size < fist_threshold

def landmark_to_servo_angle(hand_landmarks):
    servo_angle = [x_mid,y_mid,z_mid,claw_open_angle]
    WRIST = hand_landmarks.landmark[0]
    INDEX_FINGER_MCP = hand_landmarks.landmark[5]
    # calculate the distance between the wrist and the index finger
    palm_size = ((WRIST.x - INDEX_FINGER_MCP.x)**2 + (WRIST.y - INDEX_FINGER_MCP.y)**2 + (WRIST.z - INDEX_FINGER_MCP.z)**2)**0.5

    if is_fist(hand_landmarks, palm_size):
        servo_angle[3] = claw_close_angle
    else:
        servo_angle[3] = claw_open_angle
    
    # calculate x angle
    distance = palm_size
    angle = (WRIST.x - INDEX_FINGER_MCP.x) / distance  # calculate the radian between the wrist and the index finger
    angle = int(angle * 180 / 3.1415926)               # convert radian to degree
    angle = clamp(angle, palm_angle_min, palm_angle_mid)
    servo_angle[0] = map_range(angle, palm_angle_min, palm_angle_mid, x_max, x_min)

    # calculate y angle
    wrist_y = clamp(WRIST.y, wrist_y_min, wrist_y_max)
    servo_angle[1] = map_range(wrist_y, wrist_y_min, wrist_y_max, y_max, y_min)

    # calculate z angle
    palm_size = clamp(palm_size, plam_size_min, plam_size_max)
    servo_angle[2] = map_range(palm_size, plam_size_min, plam_size_max, z_min, z_max)

    # float to int
    servo_angle = [int(i) for i in servo_angle]

    return servo_angle

with mp_hands.Hands(model_complexity=0, min_detection_confidence=0.5, min_tracking_confidence=0.5) as hands:
    while cap.isOpened():
        success, image = cap.read()
        if not success:
            print("Ignoring empty camera frame.")
            # If loading a video, use 'break' instead of 'continue'.
            continue

        # To improve performance, optionally mark the image as not writeable to
        # pass by reference.
        image.flags.writeable = False
        image = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
        results = hands.process(image)

        # Draw the hand annotations on the image.
        image.flags.writeable = True
        image = cv2.cvtColor(image, cv2.COLOR_RGB2BGR)
        if results.multi_hand_landmarks:
            if len(results.multi_hand_landmarks) == 1:
                # print("One hand detected")
                hand_landmarks = results.multi_hand_landmarks[0]
                servo_angle = landmark_to_servo_angle(hand_landmarks)

                if servo_angle != prev_servo_angle:
                    print("Servo angle: ", servo_angle)
                    prev_servo_angle = servo_angle
                    if not debug:
                        ser.write(bytearray(servo_angle))
            else:
                print("More than one hand detected")
            for hand_landmarks in results.multi_hand_landmarks:
                mp_drawing.draw_landmarks(
                    image,
                    hand_landmarks,
                    mp_hands.HAND_CONNECTIONS,
                    mp_drawing_styles.get_default_hand_landmarks_style(),
                    mp_drawing_styles.get_default_hand_connections_style())
        # Flip the image horizontally for a selfie-view display.
        image = cv2.flip(image, 1)
        # show servo angle
        cv2.putText(image, str(servo_angle), (10, 30), cv2.FONT_HERSHEY_SIMPLEX, 1, (0, 0, 255), 2, cv2.LINE_AA)
        cv2.imshow('Gesture Control', image)

        if write_video:
            out.write(image)
        if cv2.waitKey(5) & 0xFF == 27:
            if write_video:
                out.release()
            break


cap.release()

 