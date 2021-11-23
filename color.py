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
sensor.set_framesize(sensor.QVGA)
sensor.run(1)
lcd.rotation(2)

#blue,red,green,yellow

colour = ['blue','red','green','yellow']

colour_threshold =([27, 55, -18, 4, -39, -20],
                    [55, 64, 14, 52, -9, 3],
                    [29, 65, -109, -18, 36, 59],
                    [30, 68, -25, -10, 52, 87])
blobs = [0,0,0,0]

def blobs_output(blobs):
    for b in blobs:
        tmp=img.draw_rectangle(b[0:4])
        tmp=img.draw_cross(b[5], b[6])
        img.draw_string(b[5], b[6], colour[i],color=(255,0,0), scale=2)
        c=img.get_pixel(b[5], b[6])
        _colour = {}
        _colour['colour'] = colour[i]
        data_ = []
        data_.append(_colour)
        data_.append(blobs[0])
    uart_Port.write(str(blobs))

def show_fps():
    fps =clock.fps()
    img.draw_string(200, 1, ("%2.2ffps" %(fps)),color=(255,0,0), scale=2)

while True:
    clock.tick()
    img=sensor.snapshot()
    show_fps()

    for i in range(4):
        blobs[i] = img.find_blobs([colour_threshold[i]],area_threshold=100,pixels_threshold=500)
        if blobs[i]:
            blobs_output(blobs[i])

    lcd.display(img)
