import smbus
import time

I2C_NUM = 1 # device at /dev/i2c-1
DEVICE_ADDRESS = 0x68 # address of the MPU 6050

# addresses of registers
GYRO_XOUT_H = 0x43
GYRO_XOUT_L = 0x44
GYRO_YOUT_H = 0x45
GYRO_YOUT_L = 0x46
GYRO_ZOUT_H = 0x47
GYRO_ZOUT_L = 0x46
PWR_MGMT_1 = 0x6b

bus = smbus.SMBus(I2C_NUM)

# wake up the MPU 6050
bus.write_byte_data(DEVICE_ADDRESS, PWR_MGMT_1, 0)

for i in range(0, 10000000):
  av = 0
  for j in range(0, 6):
    av += bus.read_byte_data(DEVICE_ADDRESS, GYRO_YOUT_L)
  print(av / 6)
