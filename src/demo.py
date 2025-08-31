# LVGL Micropython demo for unix, MacOS or ESP32 board
from micropython import const  # NOQA

import lcd_bus
import task_handler
import lvgl as lv  # NOQA


_WIDTH = const(800)
_HEIGHT = const(480)

from i2c import I2C
import gt911
import rgb_display

_CTP_SCL = const(9)
_CTP_SDA = const(8)
_CTP_IRQ = const(4)

_SD_MOSI = const(11)
_SD_SCK = const(12)
_SD_MISO = const(13)

_LCD_FREQ = const(13000000)

_HSYNC_PULSE_WIDTH = const(10)
_HSYNC_BACK_PORCH = const(10)
_HSYNC_FRONT_PORCH = const(10)

_VSYNC_PULSE_WIDTH = const(10)
_VSYNC_BACK_PORCH = const(10)
_VSYNC_FRONT_PORCH = const(20)

_PCLK = const(7)
_HSYNC = const(46)
_VSYNC = const(3)
_DE = const(5)
_DISP = None
_BCKL = None
_DRST = None

i2c_bus = I2C.Bus(
    host=1,
    scl=_CTP_SCL,
    sda=_CTP_SDA,
    freq=400000,
    use_locks=False
)

i2c_device = I2C.Device(
    i2c_bus,
    dev_id=gt911.I2C_ADDR,
    reg_bits=gt911.BITS
)

_DATA15 = const(10)  # B7
_DATA14 = const(17)  # B6
_DATA13 = const(18)  # B5
_DATA12 = const(38)  # B4
_DATA11 = const(14)  # B3
_DATA10 = const(21)  # G7
_DATA9 = const(47)  # G6
_DATA8 = const(48)  # G5
_DATA7 = const(45)  # G4
_DATA6 = const(0)  # G3
_DATA5 = const(39)  # G2
_DATA4 = const(40)  # R7
_DATA3 = const(41)  # R6
_DATA2 = const(42)  # R5
_DATA1 = const(2)  # R4
_DATA0 = const(1)  # R3

bus = lcd_bus.RGBBus(
    hsync=_HSYNC,
    vsync=_VSYNC,
    de=_DE,
    pclk=_PCLK,
    data0=_DATA0,
    data1=_DATA1,
    data2=_DATA2,
    data3=_DATA3,
    data4=_DATA4,
    data5=_DATA5,
    data6=_DATA6,
    data7=_DATA7,
    data8=_DATA8,
    data9=_DATA9,
    data10=_DATA10,
    data11=_DATA11,
    data12=_DATA12,
    data13=_DATA13,
    data14=_DATA14,
    data15=_DATA15,
    freq=_LCD_FREQ,
    hsync_front_porch=_HSYNC_FRONT_PORCH,
    hsync_back_porch=_HSYNC_BACK_PORCH,
    hsync_pulse_width=_HSYNC_PULSE_WIDTH,
    vsync_front_porch=_VSYNC_FRONT_PORCH,
    vsync_back_porch=_VSYNC_BACK_PORCH,
    vsync_pulse_width=_VSYNC_PULSE_WIDTH,
)



# buf1 = bus.allocate_framebuffer(int(_WIDTH * _HEIGHT * 2 / 20), lcd_bus.MEMORY_INTERNAL)

buf1 = bus.allocate_framebuffer(int(_WIDTH * _HEIGHT * 2 / 40), lcd_bus.MEMORY_INTERNAL)
buf2 = None
display = rgb_display.RGBDisplay(
    data_bus=bus,
    display_width=_WIDTH,
    display_height=_HEIGHT,
    frame_buffer1=buf1,
    frame_buffer2=buf2,
    color_space=lv.COLOR_FORMAT.RGB565,
    rgb565_byte_swap=True
)



display.set_power(True)
display.init()
display.set_backlight(100)
indev = gt911.GT911(i2c_device)

if indev.hw_size != (_WIDTH, _HEIGHT):
    fw_config = indev.firmware_config
    fw_config.width = _WIDTH
    fw_config.height = _HEIGHT
    fw_config.save()

    del fw_config

scrn = lv.screen_active()

# lv.refr_now(scrn.get_display())
scrn.set_style_bg_color(lv.color_hex(0xFF0000), 0)

slider1 = lv.slider(scrn)
slider1.set_size(200, 50)
slider1.align(lv.ALIGN.CENTER, 0, -100)

slider2 = lv.slider(scrn)
slider2.set_size(200, 50)
slider2.align(lv.ALIGN.CENTER, 0, 100)
slider2.set_value(100, 0)

label = lv.label(scrn)
label.set_text('HELLO WORLD!')
label.align(lv.ALIGN.CENTER, 0, -50)

th = task_handler.TaskHandler()

