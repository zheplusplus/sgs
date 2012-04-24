import sys
import gateway.wsgi.main

try:
    port = int(sys.argv[1])
except:
    port = 8000
finally:
    gateway.wsgi.main.main(port)
