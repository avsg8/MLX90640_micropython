"""
`busio` - Bus protocol support like I2C and SPI
=================================================

See `CircuitPython:busio` in CircuitPython for more details.

* Author(s): cefn
"""

from adafruit_blinka import Lockable
class I2C(Lockable):
    def __init__(self, pins=('P9','P10'), frequency=100000):
        self.init(pins, frequency)

    def init(self, pins, frequency):
        self.deinit()
        from machine import I2C as _I2C
        try:
            self._i2c = _I2C(0, mode=_I2C.MASTER, pins = pins, baudrate=frequency)
        except RuntimeError:
            raise

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
                return self._i2c.writeto(address, memoryview(buffer)[start:], stop=stop)
            else:
                return self._i2c.writeto(address, memoryview(buffer)[start:end], stop=stop)
        return self._i2c.writeto(address, buffer, stop=stop)


    def writeto_then_readfrom(self, address, buffer_out, buffer_in, *, out_start=0, out_end=None, in_start=0, in_end=None, stop=False):
        return self._i2c.writeto_then_readfrom(address, buffer_out, buffer_in,
                                               out_start=out_start, out_end=out_end,
                                               in_start=in_start, in_end=in_end, stop=stop)
