import read
import time

fetch = read.InclinationFetcher()
fetch.start()
for i in range(0, 1000000):
  time.sleep(0.1)
  print(fetch.get_inclination())
fetch.stop()
