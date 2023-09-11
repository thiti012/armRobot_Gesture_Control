




```c++
int default_angle[4] = {75, 90, 90, 60};
```

```bash
cd python
pip install -r requirements.txt
pip install mediapipe
pip install serial
```



  cam_source。
 ```python
cam_source = "http://192.168.1.100:4747/video"
# 0,1 for usbcam, "http://192.168.1.165:4747/video" for webcam
 ```


```python
x_min = 0
x_mid = 75
x_max = 150

y_min = 0
y_mid = 90
y_max = 180

z_min = 10
z_mid = 90
z_max = 180

claw_open_angle = 60
claw_close_angle = 0
```


```python
debug = True
```

```python
# use angle between wrist and index finger to control x axis
palm_angle_min = -50
palm_angle_mid = 20

# use wrist y to control y axis
wrist_y_min = 0.3
wrist_y_max = 0.9

# use palm size to control z axis
plam_size_min = 0.1
plam_size_max = 0.3


fist_threshold = 7
```


```python
ser = serial.Serial('COM4', 115200)
```

```python
debug = False
```

```bash
python main.py
```