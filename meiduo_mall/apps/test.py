from random import randint

import time

sms_code = '%06d' % randint(0, 999999)

print(type(sms_code))

a = 10
for i in range(1,a):
    print(i)
    time.sleep(10)