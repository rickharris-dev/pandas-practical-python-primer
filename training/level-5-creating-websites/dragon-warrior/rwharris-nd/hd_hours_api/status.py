from datetime import datetime
from time import time, localtime, mktime, strftime, strptime
import dateutil

time = "07:30 AM EST"
new_time = mktime(strptime(time, "%I:%M %p %Z"))

print(strftime("%I:%M %p %Z"))

print(new_time)

