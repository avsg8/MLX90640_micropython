"""
A class to call different temperature functions

"""
from machine import I2C as _I2C
import busio, adafruit_mlx90640, struct, utime


class gettemp:
    def __init__(self, baudrate = 400000, pins=('P9','P10'), addr=None, i2cp = None):
        if i2cp is None:
            self.i2cp = _I2C(0)
            self.i2cp.init(_I2C.MASTER, baudrate = baudrate)
        else:
            self.i2cp = i2cp
        if addr is None:
            self.addr = self.i2cp.scan()[0]
        else:
            self.addr = addr
        self.pins = pins
        self.baudrate = baudrate

    def gettemp_mlx(self):
        pins = self.pins
        baudrate = self.baudrate
        ixc = busio.I2C(pins= pins, frequency=baudrate)
        mlx = adafruit_mlx90640.MLX90640(ixc)
        mlx.refresh_rate = adafruit_mlx90640.RefreshRate.REFRESH_0_5_HZ
        frame = [0]*768
        mlx.getFrame(frame)
        amb = [0]*834
        mlx._GetFrameData(amb)
        amb = mlx._GetTa(amb) - 8.0
        frame = [amb] + frame
        ixc.deinit()
        return frame
    def gettemp_d6t(self):
        l = 19
        val = bytearray(l)
        wv = bytearray(20)
        #
        wv[0] = 0x02; wv [1] = 0x00; wv[2] = 0x01; wv[3] = 0xee
        wv[4] = 0x05; wv [5] = 0x90; wv[6] = 0x3a; wv[7] = 0xb8 #0x05, 0x90, 0x3a, 0xb8
        wv[8] = 0x03; wv [9] = 0x00; wv[10] = 0x03; wv[11] = 0x8b #0x03, 0x00, 0x03, 0x8b
        wv[12] = 0x03; wv [13] = 0x00; wv[14] = 0x07; wv[15] = 0x97 #0x03, 0x00, 0x07, 0x97
        wv[16] = 0x02; wv [17] = 0x00; wv[18] = 0x00; wv[19] = 0xe9 #0x02, 0x00, 0x00, 0xe9
        ii=0
        for bi in wv:
            if ii in [3,7,11,15,19]:
                self.i2cp.writeto(self.addr, bi, stop = True)
            else:
                self.i2cp.writeto(self.addr, bi, stop = False)
            ii=ii+1
        utime.sleep_ms(500)
        self.i2cp.writeto(0xA, 0x4C, stop = False)
        self.i2cp.readfrom_into(0xA, val)
        self.i2cp.deinit()
        val = struct.unpack("<"+int((len(val)-1)/2)*"H",val)
        return val
