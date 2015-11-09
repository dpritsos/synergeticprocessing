

from multiprocessing.connection import Client
import socket

print 'connection'
try:
    conn = Client(('localhost', 50000), authkey="123456")
except socket.error:
    print "Connection Refused"
print 'Send Connection'
conn.send((3,4))
r = conn.recv()
print(r)