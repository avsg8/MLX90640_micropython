"""
`adafruit_mlx90640` micropython example code
================================================================================
* Author(s): Avishek Guha (avsg8, @avs_g8), ActuallyHappening
"""
import machine, micropython, time, gc   # Some libraries that we will use
from machine import I2C
from lib import busio, adafruit_mlx90640

print("Beginning ...")

time.sleep(2.0)
while True:
    try:
        ixc = busio.I2C(pins=(21, 22), frequency=400000) # read on some forum that 400KHz is the highest baudrate that 
                                                             # wipy can support reliably
        mlx = adafruit_mlx90640.MLX90640(ixc)
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_2_HZ # 2Hz or higher refresh rates produce 0s for alternate pixels, 
                                                                        # like a checkerboard pattern; maybe the microcontroller cannot
                                                                        # read as fast?
        
        gc.collect()
        gc.threshold(gc.mem_free() // 4 + gc.mem_alloc())
                                                                        
        
        import micropython
        print(f"Getting memory stats")
        micropython.mem_info()
        
        frame = [0]*768
        mlx.getFrame(frame)
        
        print("Frame received! {frame}")
        
        mn = round(min(frame),1) # minimum temp in the frame, rounded to 1 decimal
        mx = round(max(frame),1) # maximum temp in the frame, rounded to 1 decimal
        
        """To get ambient temperature of the board see adafruit_mlx90640's implementation of the method for further clarity. 
        I just copied that over here."""
        amb = [0]*834
        mlx._GetFrameData(amb)
        amb = mlx._GetTa(amb) - 8.0  # this is ambient temp in Centigrade
        amb = round(amb,1) # ambient temp in C, rounded to 1 decimal
        ixc.deinit()
        print("Max Scene Temp (°C): "+ str(mx)+", "+"Min Scene Temp (°C): "+str(mn)+", "+"Amb Temp (°C): "+ str(amb) )
        time.sleep(1.0)
        
    except Exception as e:
        print(e, end="")
        time.sleep(1.0)
        print('raising ...')
        #print(f"Self._i2c: {self._i2c=}")
        raise e

