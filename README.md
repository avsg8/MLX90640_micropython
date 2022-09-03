# MLX90640_micropython
A quick and dirty re-purposing of adafruit circuitpython library for MLX90640 IR sensor so that it can be read using micropython (e.g. QT PY ESP32-C3)

## What was done:
Using QT PY ESP32-C3, the adafruit_mlx90640 python library (and all dependencies) was installed in a target folder using thonny. The IR sensor was tested on the board by running a few basic example codes shown here: https://github.com/adafruit/Adafruit_CircuitPython_MLX90640

Once it was seen that the sensor was working satisfactorily on the basis of the drivers in the target folder, the contents of this target folder was copied over to the "lib" folder of the PyCom WiPy 3.0. Most of the imports in the original circuitpython implementation are not required for WiPy micropython (like board id checks, modules like threading etc.) and hence have been disabled/deleted for easy debugging and readability. 

The adafruit_mlx90640.py is untouched. Only the busio.py and i2c_device.py have been modified to enable reading of raw data from the sensor.

## How to use it:
Just copy the contents of esp32_example to your esp based microcontroller and boot it, making sure to place it in the root directory "/" such that `main.py` is executed. If you are connected to a console, you can see basic info being printed out (thonny console used as well as `screen` on mac. If you don't have a console, no other indicator lights are implemented.
Since this is a 'quick & dirty' implementation, mainly for a short competition, it is not robust against many kinds of errors but will still handle and report the most common errors
