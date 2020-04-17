# MLX90640_micropython
A quick and dirty re-purposing of adafruit circuitpython library for MLX90640 IR sensor so that it can be read using micropython (e.g. pycom's wipy 3.0)

## What was done:
Using a raspberry pi 3b running Raspbian 10 (buster), the adafruit_mlx90640 python library (and all dependencies) was installed in a target folder (e.g. "/home/pi/tgt_folder") with the help of pip3. The IR sensor was tested on this raspberry pi by running a few basic example codes shown here: https://github.com/adafruit/Adafruit_CircuitPython_MLX90640

Once it was seen that the sensor was working satisfactorily on the basis of the drivers in the target folder, the contents of this target folder was copied over to the "lib" folder of the PyCom WiPy 3.0. Most of the imports in the original circuitpython implementation are not required for WiPy micropython (like board id checks, modules like threading etc.) and hence have been disabled/deleted for easy debugging and readability. 

The adafruit_mlx90640.py is untouched. Only the busio.py and i2c_device.py have been modified to enable reading of raw data from the sensor.

## How to use it:
Just copy the contents of wipy_example to your WiPy 3.0 and boot the microcontroller. If you are connected to a console, you can see the max, min and ambient temperatures being printed out. If you don't have a console, then the alternate flashing of the blue and green led means it is successfully reading data. A red flash means an error occured. 
