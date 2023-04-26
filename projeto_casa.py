#os pinos sao colocados com (GP numero definido) exemplo Pin(0,Pin.IN)...GP0 é o pino definido

#adiciona a instancia "Pin" da biblioteca "machine" ao codigo
from machine import Pin

#adicionar a biblioteca do RFID
from mfrc522 import MFRC522

#adiciona a funcao "sleep" da biblioteca "time" ao codigo
import utime

from dht import DHT11

#configura o pino conectado ao LED da placa como uma saida
led = Pin(14, Pin.OUT)   #Led no pino 14

botaoa = Pin(0, Pin.IN) 
botaob = Pin(1, Pin.IN)

dht11_pin = 2
dht11_sensor = DHT11(Pin(dht11_pin, Pin.IN))

reader = MFRC522(spi_id=0,sck=6,miso=4,mosi=7,cs=5,rst=22)

print("Iniciado!")
print("")
#executa infinitamente
while True:
    #alterando os nomes dos codigos para simplificação
    
    valora = botaoa.value()  #storing the value of the push button state in the variable logic_state
    valorb = botaob.value()
    
    reader.init()
    (stat, tag_type) = reader.request(reader.REQIDL) 
    
    if stat == reader.OK:
        (stat, uid) = reader.SelectTagSN()
        if stat == reader.OK:
            card = int.from_bytes(bytes(uid),"little",False)
            if card == 3843062025:
                #if valora == True:  #se valor do botao
                    try:
                        print("Bem vindo")
                        dht11_sensor.measure()
                        dht11_temp = dht11_sensor.temperature()
                        dht11_humid = dht11_sensor.humidity()
                        print("Temperature: {:.1f}°C   Humidity: {:.1f}% ".format(dht11_temp, dht11_humid))
                        led.high() #acende o LED
                    except OSError as e:
                        print("Erro ao ler dados do sensor:", e)
                        led.high()
                    utime.sleep(1)
            elif card != 3843062025:
                led.low()
                utime.sleep(1)
        #if valorb == True:
            #led.low()
            #print("Ate logo")
            #utime.sleep(1)
                
                
#Comentarios
#Codigo do cartao:3843062025
#Codigo do chaverinho:2250575594
    
