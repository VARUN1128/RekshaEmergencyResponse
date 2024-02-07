from machine import Pin, UART, SoftI2C
import _thread
import utime, time
import urequests
import network

i2c = SoftI2C(scl=Pin(22), sda=Pin(21), freq=10000)     #initializing the I2C method for ESP32



# WiFi settings
WIFI_SSID = "Xiaomi 11i"
WIFI_PASSWORD = "87654321"

THINGSPEAK_API_KEY = "JOY6KD80QCMACHEV"


gpsModule = UART(2, baudrate=9600)
print(gpsModule)

buff = bytearray(255)

TIMEOUT = False
FIX_STATUS = False

latitude = ""
longitude = ""
satellites = ""
GPStime = ""
BUTTON_PRESSED = False
BUTTON_NUMBER = 0
button4 = Pin(27, Pin.IN, Pin.PULL_DOWN)


def watchButton():
    global BUTTON_PRESSED, BUTTON_NUMBER, button4
    
    button1 = Pin(13, Pin.IN, Pin.PULL_DOWN)
    button2 = Pin(12, Pin.IN, Pin.PULL_DOWN)
    button3 = Pin(14, Pin.IN, Pin.PULL_DOWN)

    while True:
        try:
            if(button1.value() == 1):
                BUTTON_PRESSED = True
                BUTTON_NUMBER = 1
                print("Medical Emergency")
            elif(button2.value() == 1):
                BUTTON_PRESSED = True
                BUTTON_NUMBER = 2
                print("Fireforce")
            elif(button3.value() == 1):
                BUTTON_PRESSED = True
                BUTTON_NUMBER = 3
                print("Police")
            elif(button4.value() == 1):
                BUTTON_PRESSED = True
                BUTTON_NUMBER = 4
                print("Button 4 is pressed....Exiting")
                break
            else:
                BUTTON_PRESSED = False
                BUTTON_NUMBER = 0
            utime.sleep_ms(300)
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            break


def readGPS():
    global TIMEOUT, FIX_STATUS, latitude, longitude, satellites, GPStime,BUTTON_PRESSED, BUTTON_NUMBER
        
    def getGPS(gpsModule):
        global FIX_STATUS, TIMEOUT, latitude, longitude, satellites, GPStime
        
        timeout = time.time() + 10
        while True:

            gpsModule.readline()
            buff = str(gpsModule.readline())
            parts = buff.split(',')
        
            if (parts[0] == "b'$GPGGA" and len(parts) == 15):
                if(parts[1] and parts[2] and parts[3] and parts[4] and parts[5] and parts[6] and parts[7]):
                    
                    latitude = convertToDegree(parts[2])
                    if (parts[3] == 'S'):
                        latitude = -latitude
                    longitude = convertToDegree(parts[4])
                    if (parts[5] == 'W'):
                        longitude = -longitude
                    satellites = parts[7]
                    GPStime = parts[1][0:2] + ":" + parts[1][2:4] + ":" + parts[1][4:6]
                    FIX_STATUS = True
                    break
                    
            if (time.time() > timeout):
                TIMEOUT = True
                break
            utime.sleep_ms(500)
            
    def convertToDegree(RawDegrees):

        RawAsFloat = float(RawDegrees)
        firstdigits = int(RawAsFloat/100) 
        nexttwodigits = RawAsFloat - float(firstdigits*100) 
        
        Converted = float(firstdigits + nexttwodigits/60.0)
        Converted = '{0:.6f}'.format(Converted) 
        return str(Converted)
        
        
    while True:
        if(BUTTON_PRESSED == True and BUTTON_NUMBER == 4):
            print("Exiting GPS Monitor...")
            break

        getGPS(gpsModule)

        if(FIX_STATUS == True):
            print("Printing GPS data...")
            print(" ")
            print("Latitude: "+latitude)
            print("Longitude: "+longitude)
            print("Satellites: " +satellites)
            print("Time: "+GPStime)
            print("----------------------")
            FIX_STATUS = False
            upload_to_thingspeak(latitude, longitude, BUTTON_NUMBER)
            BUTTON_PRESSED = False

            
        if(TIMEOUT == True):
            print("No GPS data is found.")
            TIMEOUT = False



#watchButton()



def connect_to_wifi():
    sta_if = network.WLAN(network.STA_IF)
    if not sta_if.isconnected():
        print("Connecting to WiFi...")
        sta_if.active(True)
        sta_if.connect(WIFI_SSID, WIFI_PASSWORD)
        while not sta_if.isconnected():
            pass
    print("Connected to WiFi:", sta_if.ifconfig())

def upload_to_thingspeak(field1, field2,field3):
    url = "https://api.thingspeak.com/update?api_key={}&field1={}&field2={}&field3={}".format(
        THINGSPEAK_API_KEY, field1, field2,field3
    )
    response = urequests.get(url)
    print("Response:", response.text)
    response.close()


if __name__ == "__main__":
    _thread.start_new_thread(watchButton, ())
    _thread.start_new_thread(readGPS, ())

    connect_to_wifi()
