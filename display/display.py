from machine import Pin, I2C
from display.ssd1306 import SSD1306_I2C
import utime

class Display:
    def __init__ (self, i2c0_slc_pin, i2c0_sda_pin, w, h):
        self._i2c0 = I2C(0, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=100000)
        utime.sleep_ms(100)
        self._display = SSD1306_I2C(w, h, self._i2c0)
        self._display.fill(0)
        self._display.show()
    
    def show_text(self, text, x, y, color):
        # self._display.fill(0)
        self._display.text(text, x, y, color)
        self._display.show()
        utime.sleep_ms(50)
    
    def erase(self):
        self._display.fill(0)
        
