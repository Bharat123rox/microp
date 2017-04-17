import smbus
import sys
import threading
import time
import queue
import math

I2C_NUM = 1 # device at /dev/i2c-1
DEVICE_ADDRESS = 0x68 # MPU 6050 at address 0x68 of /dev/i2c-1

# address of registers
GYRO_XOUT_L = 0x44
GYRO_XOUT_H = 0x43
GYRO_YOUT_L = 0x46
GYRO_YOUT_H = 0x45
GYRO_ZOUT_L = 0x48
GYRO_ZOUT_H = 0x47
ACC_XOUT_L = 0x3c
ACC_XOUT_H = 0x3b
ACC_YOUT_L = 0x3e
ACC_YOUT_H = 0x3d
ACC_ZOUT_L = 0x40
ACC_ZOUT_H = 0x3f
POWER_MGMT_1 = 0x6b

# some constants
GYRO_DIV_SCALE_FACTOR = 131
ACC_DIV_SCALE_FACTOR = 16384

bus = smbus.SMBus(I2C_NUM)


################## basic functions #########################

def get_data(register_address):
  """ Reads a word from 'DEVICE_ADDRESS' and uses 'bus'.
      'register_address' is that of least significant byte.
  """
  bus.write_byte_data(DEVICE_ADDRESS, POWER_MGMT_1, 0)
  lsb = bus.read_byte_data(DEVICE_ADDRESS, register_address) # lsv is least significant byte
  msb = bus.read_byte_data(DEVICE_ADDRESS, register_address - 1) # msv is most significant byte. -1 because big endian
  word_value = (msb << 8) + lsb
  if (word_value > 0x8000):
    word_value = word_value - 65536 # convert from 2's complement
  return word_value

def get_scaled_acc_reading(axis):
  """ Uses constants defined in the beginning of the file
      for scaling
  """
  if (axis == "x"):
    reading = get_data(ACC_XOUT_L)
  elif (axis == "y"):
    reading = get_data(ACC_YOUT_L)
  elif (axis == "z"):
    reading = get_data(ACC_ZOUT_L)
  else:
    print("Unexpected argument to get_acc(axis) received")
    sys.exit()
  return reading / ACC_DIV_SCALE_FACTOR

def get_scaled_gyro_reading(axis):
  """ Uses constants defined in the beginning of the file
      for scaling
  """
  if (axis == "x"):
    reading = get_data(GYRO_XOUT_L)
  elif (axis == "y"):
    reading = get_data(GYRO_YOUT_L)
  elif (axis == "z"):
    reading = get_data(GYRO_ZOUT_L)
  else:
    print("Unexpected argument to get_gyro(axis) received")
    sys.exit()
  return reading / GYRO_DIV_SCALE_FACTOR

def get_inclination_using_acc(axis):
  """ Uses accelerometer readings along all axes to obtain
      inclination along required axis
  """
  def root_of_squares(a, b):
    return math.sqrt((a*a) + (b*b))

  acc_x = get_scaled_acc_reading('x')
  acc_y = get_scaled_acc_reading('y')
  acc_z = get_scaled_acc_reading('z')

  if (axis == 'x'):
    return math.degrees(math.atan2(acc_x, root_of_squares(acc_y, acc_z)))
  elif (axis == 'y'):
    return math.degrees(math.atan2(acc_y, root_of_squares(acc_z, acc_x)))
  elif (axis == 'z'):
    return math.degrees(math.atan2(acc_z, root_of_squares(acc_x, acc_y)))
  else:
    print("Unexpected argument to get_inclination_using_acc(axis) received")
    sys.exit()

#########################################################

##################### classes ###########################

class AngularAccFetcher:
  """ Instance of this can be used to fetch angular
      acceleration along three axis
      Instance variables are (no class variables exist here)
        n
          Denotes the size of array 'inst_ang_acc'
        inst_ang_acc[n]
          This array stores the values of angular acceleration
          calculated at intervals of 'ang_vel_read_interval'
          Average of all the elements in this array is used when
          angular acceleration is requested
        ang_vel_read_interval
          Two angular velocity readings (a1, a2) are obtained with time
          difference equal to 'ang_vel_read_interval' seconds and these
          an element is added/substituted to the array 'inst_ang_acc'
          with value equal to (a2 - a1) / 'ang_vel_read_interval'
        compute_thread
          The thread which represents the calculation of instantaneous
          angular acceleration and puts them in the array 'inst_ang_acc'
        should_compute
          This Boolean variable when False terminates the loop in function
          '_compute' which calculates instant instantaneous angular
          acceleration and puts them in the array 'inst_ang_acc'
  """

  def __init__(self, n, ang_vel_read_interval):
    self.n = n
    self.inst_ang_acc = [{}] * n
    self.ang_vel_read_interval = ang_vel_read_interval
    self.compute_thread = threading.Thread(target = AngularAccFetcher._compute, args = (self,))
    self.should_compute = False

  def _compute(self):
    i = 0
    print('should_compute', self.should_compute)
    while (self.should_compute):
      x1 = get_scaled_gyro_reading('x')
      y1 = get_scaled_gyro_reading('y')
      z1 = get_scaled_gyro_reading('z')
      time.sleep(self.ang_vel_read_interval)
      x2 = get_scaled_gyro_reading('x')
      y2 = get_scaled_gyro_reading('y')
      z2 = get_scaled_gyro_reading('z')
      self.inst_ang_acc[i] = {
        'x': ((x2 - x1) / self.ang_vel_read_interval),
        'y': ((y2 - y1) / self.ang_vel_read_interval),
        'z': ((z2 - z1) / self.ang_vel_read_interval)
      }
      i = ((i + 1) % (self.n))

  def start(self):
    self.should_compute = True
    self.compute_thread.start()

  def stop(self):
    self.should_compute = False

  def get_ang_acc(self):
    avx = 0
    avy = 0
    avz = 0
    for i in self.inst_ang_acc:
      if (('x' in i) and ('y' in i) and ('z' in i)):
        avx += i['x']
        avy += i['y']
        avz += i['z']
    return {
      'x': avx / self.n,
      'y': avy / self.n,
      'z': avz / self.n
    }

class InclinationFetcher:
  """ filter_gyro_weight
        A complementary filter is used to compute inclinations.
        'filter_gyro_weight' is the weight associated with the
        component that uses gyro readings to calculate current
        inclination. 1 - 'filter_gyro_weight' is the weight associated
        with the component that uses accelerometer readings to
        calculate current inclination. A linear combination of these
        two is used to obtain current inclination
      loop_interval
        The time interval between successive computations of inclination
        data. Suppose inclination data is obtained at some instant 't'.
        Next inclination data is computed at approximately 't + loop_interval'
      max_queue_size
        Maximum size of the queue. This should be selected such that
        the queue doesn't get full between successive 'get_inclination'
        calls to prevent loss of data. Loss of data would occur because
        when queue gets full, '_compute' waits until a free slot is available
        to put in the next data element, and during this waiting inclination
        data is not obtained and hence this data is lost.
      compute_thread
        The thread which represents the calculation of inclination
        along all axis and puts them in the queue 'inclinations'
      should_compute
        This Boolean variable when False terminates the loop in function
        '_compute' which calculates inclination along all axis
        and puts them in the queue 'inclinations'
  """

  def __init__(self, filter_gyro_weight = 0.7, loop_interval = 0.0001, max_queue_size = 100000):
    self.filter_gyro_weight = filter_gyro_weight
    self.loop_interval = loop_interval
    self.max_queue_size = max_queue_size
    self.should_compute = False
    self.inclinations = queue.Queue(maxsize = max_queue_size)
    self.compute_thread = threading.Thread(target = InclinationFetcher._compute, args = (self,))

  def _compute(self):
    curr_inclination = {
      'x': get_inclination_using_acc('x'),
      'y': get_inclination_using_acc('y'),
      'z': get_inclination_using_acc('z')
    }
    while (self.should_compute):
      for axis in curr_inclination:
        curr_inclination[axis] = (self.filter_gyro_weight * (curr_inclination[axis] + (get_scaled_gyro_reading(axis) * self.loop_interval))) + ((1 - self.filter_gyro_weight) * (get_inclination_using_acc(axis)))
        # Will block until free slot available in queue, if queue is full.
        self.inclinations.put(curr_inclination) 
      time.sleep(self.loop_interval)

  def start(self):
    self.should_compute = True
    self.compute_thread.start()

  def stop(self):
    self.should_compute = False

  def get_inclination(self):
    # will block until queue has some element, if queue doesn't have one
    return self.inclinations.get()


#########################################################