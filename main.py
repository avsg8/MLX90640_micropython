from network import WLAN      # For operation of WiFi network
import time, utime                   # Allows use of time.sleep() for delays
import pycom                  # Base library for Pycom devices
from umqtt import MQTTClient  # For use of MQTT protocol to talk to Adafruit IO
import ubinascii              # Needed to run any MicroPython code
import machine                # Interfaces with hardware components
import micropython            # Needed to run any MicroPython code
from machine import I2C
import struct, busio, adafruit_mlx90640, json
pycom.heartbeat(False)

# # Wireless network
WIFI_SSID = "your_wifi_ssid"
WIFI_PASS = "your_wifi_pwd" # No this is not our regular password. :)
#
# # MQTT Broker on Rpi-home
AIO_SERVER = "192.xxx.xxx.xxx"
AIO_PORT = 1883
AIO_CLIENT_ID = ubinascii.hexlify(machine.unique_id())  # Can be anything
AIO_CONTROL_FEED = "RoomCond"
#
# pycom.heartbeat(False)
#
p_out = machine.Pin('P12', mode=machine.Pin.OUT)
p_out.value(True)
# print(p_out.value())
time.sleep(0.1)
#
wlan = WLAN(mode=WLAN.STA, antenna = WLAN.EXT_ANT)
#wlan.init(mode=WLAN.AP, ssid='feluda', auth=(WLAN.WPA2,'prodoshmitter'), channel=7, antenna=WLAN.INT_ANT)
#pycom.rgbled(0x007f00)
ixc = busio.I2C(pins=('P9','P10'), frequency=800000)
mlx = adafruit_mlx90640.MLX90640(ixc)
mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ
from machine import WDT
wdt = WDT(timeout=60000)
while True:
    try:
        if wlan.isconnected()==0:
            wlan.connect(WIFI_SSID, auth=(WLAN.WPA2, WIFI_PASS), timeout=5000)
            while not wlan.isconnected():
                machine.idle() #code waits till wifi is connected
        ipadd = wlan.ifconfig()
        #print("Connected to Wifi")
        client = MQTTClient(AIO_CLIENT_ID, AIO_SERVER, AIO_PORT)#, AIO_USER, AIO_KEY)
        pycom.rgbled(0xff0000)
        #major work happends here! Fingers crossed
        frame = [0]*768
        mlx.getFrame(frame)
        mn = round(min(frame),1)
        mx = round(max(frame),1)
        amb = [0]*834
        mlx._GetFrameData(amb)
        amb = mlx._GetTa(amb) - 8.0
        data = {}
        data["frame"] = frame
        data = json.dumps(data)
        pycom.rgbled(0x00ff00)
        if max(frame)>27.0:
            client.connect()
            #client.publish(AIO_CONTROL_FEED, str(mx)+","+str(mn))
            client.publish(AIO_CONTROL_FEED, data)
            #print("Connected to %s, subscribed to %s topic" % (AIO_SERVER, AIO_CONTROL_FEED))
            client.disconnect()
        print(amb)
        #time.sleep(20.0)
        wdt.feed()
        #machine.deepsleep(10000)
    except Exception as e:
        client.connect()
        client.publish(AIO_CONTROL_FEED, "something went wrong. Let's try again")
        client.disconnect()
        #time.sleep(5.0)
        pass
