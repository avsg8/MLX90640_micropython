"""
`adafruit_mlx90640` micropython example code
================================================================================
* Author(s): Avishek Guha (avsg8, @avs_g8)
"""
import pycom, machine, micropython, time   # Some libraries that we will use
from machine import I2C
import busio, adafruit_mlx90640

pycom.heartbeat(False) #switch off heartbeat

time.sleep(2.0)
while True:
    try:
        pycom.rgbled(0x0000ff) #inidicates start of code block by red led
        ixc = busio.I2C(pins=('P9','P10'), frequency=400000)
        mlx = adafruit_mlx90640.MLX90640(ixc)
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ # refresh rates high
        frame = [0]*768
        mlx.getFrame(frame)
        mn = round(min(frame),1) # minimum temp in the frame, rounded to 1 decimal
        mx = round(max(frame),1) # maximum temp in the frame, rounded to 1 decimal
        """
        To get ambient temperature of the board see adafruit_mlx90640's implementation of the method

        """
        amb = [0]*834
        mlx._GetFrameData(amb)
        amb = mlx._GetTa(amb) - 8.0  # this is ambient temp in Centigrade
        amb = round(amb,1) # ambient temp in C, rounded to 1 decimal
        pycom.rgbled(0x00ff00) # inidicates successful execution of code
        ixc.deinit()
        print("Max Scene Temp (°C): "+ str(mx)+", "+"Min Scene Temp (°C): "+str(mn)+", "+"Amb Temp (°C): "+ str(amb) )
        time.sleep(1.0)
    except Exception as e:
        print(e)
        pycom.rgbled(0xff0000) # indicates some error occured
