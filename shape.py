# identify the rectangle
import sensor
import image
import lcd
import time
from Maix import GPIO
from fpioa_manager import fm, board_info
from machine import UART
clock = time.clock()
fm.register(34, fm.fpioa.UART2_TX, force=True)
fm.register(35, fm.fpioa.UART2_RX, force=True)
uart_Port = UART(UART.UART2, 115200,8,0,0, timeout=1000, read_buf_len= 4096)
lcd.init()
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QQVGA)
sensor.run(1)
lcd.rotation(2)
def uart_write(i):
    data_ = []
    data_.append(blobs[i])
    uart_Port.write(str(data_))
while True:
    img=sensor.snapshot()
    RECT = img.find_rects(threshould = 10000)
    if RECT:
        for b in RECT:
            img.draw_rectangle(b.rect(),color =(255,0,0))
            for p in b.corners():
                img.draw_circle(p[0],p[1],3,color = (0,255,0))
            c=img.get_pixel(b[0], b[1])
    lcd.display(img)
    
    
# identify the circle
import sensor, image, time, lcd
sensor.reset()
sensor.set_pixformat(sensor.RGB565)
sensor.set_framesize(sensor.QVGA)
sensor.skip_frames(time = 300)
sensor.run(1)
lcd.init()
lcd.rotation(2)
clock = time.clock()
while(True):
    clock.tick()
    img = sensor.snapshot()
    for c in img.find_circles(threshold = 1800, x_margin = 20, y_margin = 20, r_margin = 20,
            r_min = 5, r_max = 45, r_step = 20):
        img.draw_circle(c.x(), c.y(), c.r(), color = (255, 0, 0))#识别到的红色圆形用红色的圆框出来
    print("r %f" % c.r())
    print("FPS %f" % clock.fps())
    lcd.display(img)
