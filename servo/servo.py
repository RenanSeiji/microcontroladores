from machine import Pin,PWM

class Servo:
    def __init__ (self, pin, freq):
        self._servo = PWM(Pin(pin))
        self._servo.freq(freq)
    
    def set_servo (self, position):
        angulo = int( (position - 0) * (7850 - 1310) )
        angulo = int( angulo / (180 - 0) + 1310 )
        self._servo.duty_u16(angulo)
