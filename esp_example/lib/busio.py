
"""
---------------------------------------------------------------------------------------------------------------------------------------
Please note: The following code has been modified from its original form at certain places so that it can work with Wipy3.0 micropython
---------------------------------------------------------------------------------------------------------------------------------------
================================================================================
* Author(s): Avishek Guha (avsg8, @avs_g8)
"""

"""
`busio` - Bus protocol support like I2C and SPI
=================================================

See `CircuitPython:busio` in CircuitPython for more details.

* Author(s): cefn
"""

from adafruit_blinka import Lockable
import machine
class I2C(Lockable):
    def __init__(self, pins=(21, 22), frequency=100000):
        self.init(pins, frequency)

    def init(self, pins, frequency):
        self.deinit()
        from machine import I2C as _I2C
        self._pins = (machine.Pin(int(pins[0])), machine.Pin(int(pins[1])))
        
        try:
            #_newI2C = _I2C(0, scl=machine.Pin(21), sda=machine.Pin(22))
            #print(f"new i2c: {_newI2C=}")
            #self._i2c = _newI2C
            #print(f"Self._i2c after: {self._i2c=}")
            self._i2c = _I2C(0, scl=self._pins[0], sda=self._pins[1], freq=frequency)
        except RuntimeError:
            raise
        print(f"Created i2c: {self._i2c}")

    def deinit(self):
        try:
            del self._i2c
        except AttributeError:
            pass

    # def __enter__(self):
    #     self._lock.acquire()
    #     return self
    #
    # def __exit__(self, exc_type, exc_value, traceback):
    #     self._lock.release()
    #     self.deinit()

    def scan(self):
        return self._i2c.scan()

    def readfrom_into(self, address, buffer, *, start=0, end=None):
        if start is not 0 or end is not None:
            if end is None:
                end = len(buffer)
            buffer = memoryview(buffer)[start:end]
        stop = True  # remove for efficiency later
        return self._i2c.readfrom_into(address, buffer)

    def writeto(self, address, buffer, *, start=0, end=None, stop=True):
        if isinstance(buffer, str):
            buffer = bytes([ord(x) for x in buffer])
        if start is not 0 or end is not None:
            if end is None:
                return self._i2c.writeto(address, memoryview(buffer)[start:], stop)
            else:
                return self._i2c.writeto(address, memoryview(buffer)[start:end], stop)
        return self._i2c.writeto(address, buffer, stop)

    """
    The following method does not exist in wipy3.0 micropython. To minimize code chopping, we will keep it, but just change line 72 of i2c_device.py to "false" in te __init__ method
    """
    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        return self._i2c.writeto_then_readfrom(address, buffer_out, buffer_in,
                                               out_start=out_start, out_end=out_end,
                                               in_start=in_start, in_end=in_end, stop=stop)

