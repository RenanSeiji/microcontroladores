#====================================(imports iniciais)====================================================================
#adiciona a instancia "Pin", "PWM", "UART" e "I2C" da biblioteca "machine" ao codigo
from machine import Pin, UART, PWM, I2C

#adicionar a biblioteca do RFID
from mfrc522 import MFRC522

#adiciona a funcao "sleep" da biblioteca "time" ao codigo
import utime

#biblioteca do sensor de temp. umid.
from dht import DHT11

# Importa a classe SSD1306_I2C da biblioteca ssd1306.py
from display.ssd1306 import SSD1306_I2C

from buzzer.buzzer import Buzzer

#=======================================(pinagens)====================================================================
#conectado ao LED da placa como uma saida
led = Pin(14, Pin.OUT)   #Led no pino 14

#Botao
botaob = Pin(1, Pin.IN)

#Sensor DHT
dht11_pin = 2
dht11_sensor = DHT11(Pin(dht11_pin, Pin.IN))

#Servo motor
servo = PWM(Pin(16))
servo.freq(50)

#RFID
reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

# Define os pinos do Raspberry Pi Pico conectados ao barramento I2C 0
i2c0_slc_pin = 9
i2c0_sda_pin = 8

buzzer = Buzzer(15)

#=======================================(configurações)====================================================================

#Mapeando o servo motor para posicionar os valores em angulo
def setServo (position):
    angulo = int( (position - 0) * (7850 - 1310) )
    angulo = int( angulo / (180 - 0) + 1310 )
    servo.duty_u16(angulo)

#Print para a inicialização do projeto e saber que nao deu nenhum erro
print("Iniciado!")
print("")

# Inicializa o I2C0 com os pinos GPIO9 (SCL) e GPIO8 (SDA)
i2c0 = I2C(0, scl=Pin(i2c0_slc_pin), sda=Pin(i2c0_sda_pin), freq=100000)

utime.sleep_ms(100)

# Inicializa o display OLED I2C de 128x64
display = SSD1306_I2C(128, 32, i2c0)

# Limpa o display
display.fill(0)
display.show()

# preenche toda a tela com cor = 0
display.fill(0)

#========================================(Programa principal)==============================================================
while True:
    #guardar o valor do estado do botao
    valorb = botaob.value() 
    
    reader.init() #iniciar o RFID
    (stat, tag_type) = reader.request(reader.REQIDL)
    
    display.fill(0)
    
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
#==============================================(If do cartao)==============================================================
            if card == 3843062025: #Codigo do cartao
                    try:
                        print("")
                        print("Bem vindo Renan")
                        display.text('Bem vindo Renan', 0, 0, 1)  # desenha algum texto em x = 40, y = 0 , cor = 1
                        #servo em angulo
                        setServo(90)
                        #sensor de umid e temp
                        dht11_sensor.measure()
                        dht11_temp = dht11_sensor.temperature()
                        dht11_humid = dht11_sensor.humidity()
                        print("Temperature: {:.1f}°C   Humidity: {:.1f}% ".format(dht11_temp, dht11_humid))
                        display.text("Temp: {:.1f}C ".format(dht11_temp), 0, 12, 1)  # desenha algum texto em x = 40, y = 0 , cor = 1
                        display.text("Humid: {:.1f}% ".format(dht11_humid), 0, 24, 1)
                        display.show()
                        utime.sleep_ms(100)
                        buzzer.song1()
                        led.high() #acende o LED
                    except OSError as e: #caso der erro na leitura do sensor
                        print("Erro ao ler dados do sensor:", e)
                        led.high()
                    utime.sleep(1)
#=================================================(If do chaverinho)=======================================================
            elif card == 2250575594:
                    try:
                        print("")
                        print("Bem vindo Arthur")
                        display.text('Bem vindo Arthur', 0, 0, 1)  # desenha algum texto em x = 40, y = 0 , cor = 1
                        #servo em angulo
                        setServo(80)
                        #sensor de umid e temp
                        dht11_sensor.measure()
                        dht11_temp = dht11_sensor.temperature()
                        dht11_humid = dht11_sensor.humidity()
                        print("Humidity: {:.1f}°C   Temperature: {:.1f}% ".format(dht11_humid, dht11_temp))
                        display.text("Temp: {:.1f}C ".format(dht11_temp), 0, 12, 1)  # desenha algum texto em x = 40, y = 0 , cor = 1
                        display.text("Humid: {:.1f}% ".format(dht11_humid), 0, 24, 1)
                        display.show()
                        utime.sleep_ms(100)
                        buzzer.song1()
                        led.high() #acende o LED
                    except OSError as e: #caso der erro na leitura do sensor
                        print("Erro ao ler dados do sensor:", e)
                        led.high()
                    utime.sleep(1)
#==============================================(If nao for nenhum dos dois)=================================================
            elif card != 3843062025 and card != 2250575594:
                print("ID nao identificado")
                display.text('ID nao identificado', 0, 0, 1)  # desenha algum texto em x = 40, y = 0 , cor = 1
                display.show()
                led.low()
                setServo(0)
                utime.sleep(1)
#===========================================(Botao para reset)=============================================================                
    elif valorb == True:
        led.low()
        print("Ate logo")
        setServo(0)
        display.fill(0)
        display.show()
        utime.sleep(1)
                
                
#===========================================(Comentarios)==================================================================
#os pinos sao colocados com (GP numero definido) exemplo Pin(0,Pin.IN)...GP0 é o pino definido
#Codigo do cartao:3843062025
#Codigo do chaverinho:2250575594

#===========================================(Pinagens)=====================================================================
#Led         GP14
#Motor       GP16
#Botao       GP1
#DHT11       GP2
#DisplaySCL  GP9
#DisplaySDA  GP8
#RFID(MISO)  GP4
#RFID(MOSI)  GP7
#RFID(SCK)   GP6
#RFID(SDA)   GP5