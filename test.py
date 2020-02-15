import uuid
import requests
from datetime import datetime
import time


mac = ''.join(['{:02x}'.format((uuid.getnode() >> ele) & 0xff) for ele in range(0, 8*6, 8)][::-1])
print(mac)

a = str(datetime.now())
print(datetime.today())
print(a)
datetime_object = datetime.strptime(a, '%Y-%m-%d %I:%M:%S.%f')

assert(datetime_object < datetime.today())



