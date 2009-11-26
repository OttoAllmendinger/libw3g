import sys
import time

print 'Content-Type: text/html'
print

for n in range(30):
    sys.stdout.write(str(n))
    sys.stdout.flush()
    time.sleep(0.1)
