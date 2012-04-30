import sys
import gateway.server

try:
    port = int(sys.argv[1])
except:
    port = 8000
finally:
    gateway.server.start(port)
