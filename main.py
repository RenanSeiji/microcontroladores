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
from ssd1306 import SSD1306_I2C

#=======================================(pinagens)====================================================================
#conectado ao LED da placa como uma saida
led = Pin(14, Pin.OUT)   #Led no pino 14

#Definir pino para o Botao
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

# Definir o pino para o buzzer
buzzer = PWM(Pin(15))
#=======================================(configuração das notas)====================================================================
tones = {
"B0": 31,
"C1": 33,
"CS1": 35,
"D1": 37,
"DS1": 39,
"E1": 41,
"F1": 44,
"FS1": 46,
"G1": 49,
"GS1": 52,
"A1": 55,
"AS1": 58,
"B1": 62,
"C2": 65,
"CS2": 69,
"D2": 73,
"DS2": 78,
"E2": 82,
"F2": 87,
"FS2": 93,
"G2": 98,
"GS2": 104,
"A2": 110,
"AS2": 117,
"B2": 123,
"C3": 131,
"CS3": 139,
"D3": 147,
"DS3": 156,
"E3": 165,
"F3": 175,
"FS3": 185,
"G3": 196,
"GS3": 208,
"A3": 220,
"AS3": 233,
"B3": 247,
"C4": 262,
"CS4": 277,
"D4": 294,
"DS4": 311,
"E4": 330,
"F4": 349,
"FS4": 370,
"G4": 392,
"GS4": 415,
"A4": 440,
"AS4": 466,
"B4": 494,
"C5": 523,
"CS5": 554,
"D5": 587,
"DS5": 622,
"E5": 659,
"F5": 698,
"FS5": 740,
"G5": 784,
"GS5": 831,
"A5": 880,
"AS5": 932,
"B5": 988,
"C6": 1047,
"CS6": 1109,
"D6": 1175,
"DS6": 1245,
"E6": 1319,
"F6": 1397,
"FS6": 1480,
"G6": 1568,
"GS6": 1661,
"A6": 1760,
"AS6": 1865,
"B6": 1976,
"C7": 2093,
"CS7": 2217,
"D7": 2349,
"DS7": 2489,
"E7": 2637,
"F7": 2794,
"FS7": 2960,
"G7": 3136,
"GS7": 3322,
"A7": 3520,
"AS7": 3729,
"B7": 3951,
"C8": 4186,
"CS8": 4435,
"D8": 4699,
"DS8": 4978
}

song = ["E5","P","G5","P","A5","P","P","E5","P","G5","P","AS5","A5","P","P","P","E5","P","G5","P","A5","P","P","G5","P","E5"]
#=======================================(configurações)====================================================================

#Mapeando o servo motor para posicionar os valores em angulo
def setServo (position):
    angulo = int( (position - 0) * (7850 - 1310) )
    angulo = int( angulo / (180 - 0) + 1310 )
    servo.duty_u16(angulo)
def song1 (song):
    for i in range(len(song)):
        if (song[i] == "P"):
            pause()
        else:
            playtone(tones[song[i]])
        utime.sleep(0.3)
    pause()
        
def pause ():
    buzzer.duty_u16(0)
def playtone (freq):
    buzzer.duty_u16(1000)
    buzzer.freq(freq)

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
                        song1(song)
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